# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/utils.py
# Compiled at: 2009-07-20 09:57:48
from lxml import etree
import ntriples, StringIO, simplejson
SPARQLNS = 'http://www.w3.org/2005/sparql-results#'

def parse_sparql_result(xml):
    doc = etree.fromstring(xml)
    results = []
    for result in doc.xpath('/s:sparql/s:results/s:result', namespaces={'s': SPARQLNS}):
        data = {}
        for binding in result:
            name = unicode(binding.attrib['name'])
            for value in binding:
                type = unicode(value.tag.split('}')[(-1)])
                lang = value.attrib.get('{http://www.w3.org/XML/1998/namespace}lang')
                datatype = value.attrib.get('datatype')
                text = value.text
                if text is not None and not isinstance(text, unicode):
                    text = text.decode('utf8')
                if type == 'uri':
                    if text.startswith('<'):
                        text = text[1:]
                    if text.endswith('>'):
                        text = text[:-1]
                data[name] = {'value': text, 'type': type}
                if lang is not None:
                    data[name]['lang'] = lang.decode('utf8')
                if datatype is not None:
                    data[name]['datatype'] = datatype.decode('utf8')

        results.append(data)

    if not results:
        bools = doc.xpath('/s:sparql/s:boolean/text()', namespaces={'s': SPARQLNS})
        if bools:
            if bools[0] == 'true':
                return True
            else:
                return False
    return results


def ntriples_to_dict(file):

    class TripleDict(dict):

        def triple(self, s, p, o):
            if isinstance(s, ntriples.URI):
                subject = unicode(s)
            elif isinstance(s, ntriples.bNode):
                subject = '_:%s' % s
            else:
                raise ValueError('Unknown subject type: %s' % type(s))
            predicate = unicode(p)
            predicates = self.get(subject, {})
            values = predicates.get(predicate, [])
            value = {'value': unicode(o)}
            if isinstance(o, ntriples.URI):
                value['type'] = 'uri'
            elif isinstance(o, ntriples.bNode):
                value['type'] = 'bnode'
            elif isinstance(o, ntriples.Literal):
                (lang, dtype, literal) = o.split(' ', 2)
                value['type'] = 'literal'
                value['value'] = literal
                if lang != 'None':
                    value['lang'] = lang
                elif dtype != 'None':
                    value['datatype'] = dtype
            else:
                raise ValueError('Unknown object type: %s' % type(o))
            values.append(value)
            self[subject] = predicates
            predicates[predicate] = values

    parser = ntriples.NTriplesParser(TripleDict())
    result = parser.parse(file)
    return dict(result)


def dict_to_ntriples(data):
    result = StringIO.StringIO()
    for (subject, predicates) in data.items():
        if not subject.startswith('_:'):
            subject = '<%s>' % subject
        for (predicate, values) in predicates.items():
            predicate = '<%s>' % predicate
            for value in values:
                if value['type'] == 'uri':
                    object = '<%s>' % value['value']
                elif value['type'] == 'bnode':
                    object = '_:%s' % value['value']
                else:
                    object = value['value']
                    object = object.replace('\\', '\\\\')
                    object = object.replace('\t', '\\t')
                    object = object.replace('\n', '\\n')
                    object = object.replace('\r', '\\r')
                    object = object.replace('"', '\\"')
                    object = '"%s"' % object
                    if value.get('lang'):
                        object = '%s@%s' % (object, value['lang'])
                    elif value.get('datatype'):
                        object = '%s^^<%s>' % (object, value['datatype'])
                ntriple = '%s %s %s .\n' % (subject, predicate, object)
                result.write(ntriple)

    result.seek(0)
    return result


def json_to_ntriples(data):
    data = simplejson.load(data)
    return dict_to_ntriples(data)


def ntriples_to_json(triples):
    data = ntriples_to_dict(triples)
    return StringIO.StringIO(simplejson.dumps(data, indent=True))