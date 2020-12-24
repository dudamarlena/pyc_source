# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/rdf/_namespace.py
# Compiled at: 2008-03-16 19:10:10
"""
This module defines namespace related classes and functions and a few
standard namespace instances.

"""
from rdf.term import URIRef
import logging
_logger = logging.getLogger(__name__)

class Namespace(URIRef):

    def term(self, name):
        return URIRef(self + name)

    def __getitem__(self, key, default=None):
        return self.term(key)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        else:
            return self.term(name)


class NamespaceDict(dict):

    def __new__(cls, uri=None, context=None):
        inst = dict.__new__(cls)
        inst.uri = uri
        inst.__context = context
        return inst

    def __init__(self, uri, context=None):
        self.uri = uri
        self.__context = context

    def term(self, name):
        uri = self.get(name)
        if uri is None:
            uri = URIRef(self.uri + name)
            if self.__context and (uri, None, None) not in self.__context:
                _logger.warning('%s not defined' % uri)
            self[name] = uri
        return uri

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        else:
            return self.term(name)

    def __getitem__(self, key, default=None):
        return self.term(key) or default

    def __str__(self):
        return self.uri

    def __repr__(self):
        return "rdf.NamespaceDict('%s')" % str(self.uri)


class ClosedNamespace(object):
    """
    
    """

    def __init__(self, uri, terms):
        self.uri = uri
        self.__uris = {}
        for t in terms:
            self.__uris[t] = URIRef(self.uri + t)

    def term(self, name):
        uri = self.__uris.get(name)
        if uri is None:
            raise Exception("term '%s' not in namespace '%s'" % (name, self.uri))
        else:
            return uri
        return

    def __getitem__(self, key, default=None):
        return self.term(key)

    def __getattr__(self, name):
        if name.startswith('__'):
            raise AttributeError
        else:
            return self.term(name)

    def __str__(self):
        return self.uri

    def __repr__(self):
        return "rdf.ClosedNamespace('%s')" % str(self.uri)


RDF = ClosedNamespace(URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#'), [
 'RDF', 'Description', 'ID', 'about', 'parseType', 'resource', 'li', 'nodeID', 'datatype',
 'Seq', 'Bag', 'Alt', 'Statement', 'Property', 'XMLLiteral', 'List',
 'subject', 'predicate', 'object', 'type', 'value', 'first', 'rest',
 'nil'])
RDF.RDFNS = RDF.uri
RDFS = ClosedNamespace(URIRef('http://www.w3.org/2000/01/rdf-schema#'), [
 'Resource', 'Class', 'subClassOf', 'subPropertyOf', 'comment', 'label',
 'domain', 'range', 'seeAlso', 'isDefinedBy', 'Literal', 'Container',
 'ContainerMembershipProperty', 'member', 'Datatype'])
RDFS.RDFSNS = RDFS.uri
from unicodedata import category, decomposition
NAME_START_CATEGORIES = [
 'Ll', 'Lu', 'Lo', 'Lt', 'Nl']
NAME_CATEGORIES = NAME_START_CATEGORIES + ['Mc', 'Me', 'Mn', 'Lm', 'Nd']
ALLOWED_NAME_CHARS = ['·', '·', '-', '.', '_']

def is_ncname(name):
    """
    TODO:
    """
    if name is None or name == '':
        return False
    first = name[0]
    if first == '_' or category(first) in NAME_START_CATEGORIES:
        for i in xrange(1, len(name)):
            c = name[i]
            if category(c) not in NAME_CATEGORIES:
                if c in ALLOWED_NAME_CHARS:
                    continue
                return 0

        return 1
    else:
        return 0
    return


XMLNS = 'http://www.w3.org/XML/1998/namespace'

def split_uri(uri):
    if uri.startswith(XMLNS):
        return (
         XMLNS, uri.split(XMLNS)[1])
    length = len(uri)
    for i in xrange(0, length):
        c = uri[(-i - 1)]
        if category(c) not in NAME_CATEGORIES:
            if c in ALLOWED_NAME_CHARS:
                continue
            for j in xrange(-1 - i, length):
                if category(uri[j]) in NAME_START_CATEGORIES or uri[j] == '_':
                    ns = uri[:j]
                    if not ns:
                        break
                    ln = uri[j:]
                    return (ns, ln)

            break

    raise Exception("Can't split '%s'" % uri)