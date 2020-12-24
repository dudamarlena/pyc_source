# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/helpers/stream.py
# Compiled at: 2008-08-22 15:02:55
import sys, pickle, golem, generics
from lxml import etree
import md5

class Mapping(dict, generics.ns_dict_mixin):
    __module__ = __name__

    def __init__(self, dictionaryfile, dictionarynamespace):
        self.dictionary = self.namespaced_dictionary(dictionaryfile, dictionarynamespace)

    def assign(self, d):
        for key in d:
            self[key] = d[key]


class Stream(object):
    __module__ = __name__

    def __init__(self, mappings):
        self.mappings = mappings
        self.data = None
        self.cached_tree = None
        self.cached_tree_md5 = None
        return

    def process(self, filename, onXML=False, onValues=True):
        try:
            fdata = filename.read()
            f = filename
        except AttributeError:
            f = open(filename, 'r')
            fdata = f.read()

        md5sum = md5.new(fdata).hexdigest()
        if md5sum != self.cached_tree_md5:
            f.seek(0)
            tree = etree.parse(f)
            self.cached_tree = tree
            self.cached_tree_md5 = md5sum
        else:
            tree = self.cached_tree
        result = ''
        for key in self.mappings:
            address = key.split(',')
            processor = self.mappings[key]
            concepts = golem.db.conceptlist(*[ self.mappings.dictionary.concept(c) for c in address ])
            xpath = golem.helpers.xpath.xpath(concepts)
            sanitized_addr = address[(-1)].replace(':', '_')
            sanitized_addr = sanitized_addr.replace('/', '_over_')
            sanitized_addr = sanitized_addr.replace('\\', '_backslash_')
            sanitized_addr = sanitized_addr.replace('%', '_pct')
            namespace = self.mappings.dictionary.d.dnamespace
            if not (namespace.endswith('#') or namespace.endswith('/')):
                uri = '{%s#}%s' % (namespace, sanitized_addr)
            else:
                uri = '{%s}%s' % (namespace, sanitized_addr)

            class Result(list):
                __module__ = __name__
                __slots__ = ['filename', 'uri']

                def __init__(self, data, filename=None, uri=None):
                    self.filename = filename
                    self.uri = uri
                    list.__init__(self, data)

            res = Result([], filename=filename, uri=uri)
            for x in xpath:
                nodes = tree.xpath(x, namespaces=golem.namespaces)
                res.extend(tree.xpath(x, namespaces=golem.namespaces))

            if onXML:
                result += processor(res)
                result += '\n'
            elif onValues:
                try:
                    pres = Result([ concepts[(-1)].getvalue(x) for x in res ], filename=res.filename, uri=res.uri)
                    result += processor(pres)
                except AttributeError, e:
                    id = concepts[(-1)].id
                    print >> sys.stderr, 'Skipping id', id, '- no assigned getvalue template in dictionary'
                except ValueError:
                    print >> sys.stderr, 'Malformed data in %s - skipping.' % concepts[(-1)].id

        self.result = result
        return result