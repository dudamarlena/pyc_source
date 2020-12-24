# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/sparql/results/jsonresults.py
# Compiled at: 2012-02-24 05:27:21
from rdflib.query import Result, ResultException, ResultSerializer, ResultParser
from rdflib import Literal, URIRef, BNode
import jsonlayer

class JSONResultParser(ResultParser):

    def parse(self, source):
        return JSONResult(jsonlayer.decode(source.read()))


class JSONResultSerializer(ResultSerializer):

    def __init__(self, result):
        ResultSerializer.__init__(self, result)

    def serialize(self, stream, encoding=None):
        res = {}
        if self.result.type == 'ASK':
            res['head'] = {}
            res['boolean'] = self.result.askAnswer
        else:
            res['results'] = {}
            res['head'] = {}
            res['head']['vars'] = self.result.vars
            res['results']['bindings'] = [ self._bindingToJSON(x) for x in self.result.bindings ]
        r = jsonlayer.encode(res)
        if encoding != None:
            stream.write(r.encode(encoding))
        else:
            stream.write(r)
        return

    def _bindingToJSON(self, b):
        res = {}
        for var in b:
            j = termToJSON(self, b[var])
            if j != None:
                res[var] = termToJSON(self, b[var])

        return res


class JSONResult(Result):

    def __init__(self, json):
        self.json = json
        if 'boolean' in json:
            type_ = 'ASK'
        elif 'results' in json:
            type_ = 'SELECT'
        else:
            raise ResultException('No boolean or results in json!')
        Result.__init__(self, type_)
        if type_ == 'ASK':
            self.askAnswer = bool(json['boolean'])
        else:
            self.bindings = self._get_bindings()

    def _get_bindings(self):
        ret = []
        for row in self.json['results']['bindings']:
            outRow = {}
            for k, v in row.items():
                outRow[k] = parseJsonTerm(v)

            ret.append(outRow)

        return ret


def parseJsonTerm(d):
    """rdflib object (Literal, URIRef, BNode) for the given json-format dict.
    
    input is like:
      { 'type': 'uri', 'value': 'http://famegame.com/2006/01/username' }
      { 'type': 'literal', 'value': 'drewp' }
    """
    t = d['type']
    if t == 'uri':
        return URIRef(d['value'])
    if t == 'literal':
        if 'xml:lang' in d:
            return Literal(d['value'], lang=d['xml:lang'])
        return Literal(d['value'])
    if t == 'typed-literal':
        return Literal(d['value'], datatype=URIRef(d['datatype']))
    if t == 'bnode':
        return BNode(d['value'])
    raise NotImplementedError('json term type %r' % t)


def termToJSON(self, term):
    if isinstance(term, URIRef):
        return {'type': 'uri', 'value': str(term)}
    else:
        if isinstance(term, Literal):
            if term.datatype != None:
                return {'type': 'typed-literal', 'value': unicode(term), 
                   'datatype': str(term.datatype)}
            else:
                r = {'type': 'literal', 'value': unicode(term)}
                if term.language != None:
                    r['xml:lang'] = term.language
                return r

        else:
            if isinstance(term, BNode):
                return {'type': 'bnode', 'value': str(term)}
            if term == None:
                return
            raise ResultException('Unknown term type: %s (%s)' % (term, type(term)))
        return