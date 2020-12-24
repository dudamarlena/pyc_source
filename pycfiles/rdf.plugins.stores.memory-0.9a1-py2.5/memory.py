# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/memory.py
# Compiled at: 2008-04-06 18:32:55
"""A in-memory store plugin for the rdf pacakge.

This is a plugin for rdf.plugins.stores package. See::

    http://pypi.python.org/pypi/rdf/ 

for more information on the Python rdf package.

"""
__version__ = '0.9a1'
ANY = None
from rdf.store import Store

class Memory(Store):
    """An in memory implementation of a triple store.

This triple store uses nested dictionaries to store triples. Each
triple is stored in two such indices as follows spo[s][p][o] = 1 and
pos[p][o][s] = 1.
    """

    def __init__(self, configuration=None, identifier=None):
        super(Memory, self).__init__(configuration)
        self.identifier = identifier
        self.__spo = {}
        self.__pos = {}
        self.__osp = {}
        self.__namespace = {}
        self.__prefix = {}

    def add(self, (subject, predicate, object), context, quoted=False):
        """        Add a triple to the store of triples.
        """
        spo = self.__spo
        try:
            po = spo[subject]
        except:
            po = spo[subject] = {}

        try:
            o = po[predicate]
        except:
            o = po[predicate] = {}

        o[object] = 1
        pos = self.__pos
        try:
            os = pos[predicate]
        except:
            os = pos[predicate] = {}

        try:
            s = os[object]
        except:
            s = os[object] = {}

        s[subject] = 1
        osp = self.__osp
        try:
            sp = osp[object]
        except:
            sp = osp[object] = {}

        try:
            p = sp[subject]
        except:
            p = sp[subject] = {}

        p[predicate] = 1

    def remove(self, (subject, predicate, object), context=None):
        for ((subject, predicate, object), c) in self.triples((subject, predicate, object)):
            del self.__spo[subject][predicate][object]
            del self.__pos[predicate][object][subject]
            del self.__osp[object][subject][predicate]

    def triples(self, (subject, predicate, object), context=None):
        """A generator over all the triples matching """
        if subject != ANY:
            spo = self.__spo
            if subject in spo:
                subjectDictionary = spo[subject]
                if predicate != ANY:
                    if predicate in subjectDictionary:
                        if object != ANY:
                            if object in subjectDictionary[predicate]:
                                yield (
                                 (
                                  subject, predicate, object), self.__contexts())
                        else:
                            for o in subjectDictionary[predicate].keys():
                                yield (
                                 (
                                  subject, predicate, o), self.__contexts())

                else:
                    for p in subjectDictionary.keys():
                        if object != ANY:
                            if object in subjectDictionary[p]:
                                yield (
                                 (
                                  subject, p, object), self.__contexts())
                        else:
                            for o in subjectDictionary[p].keys():
                                yield (
                                 (
                                  subject, p, o), self.__contexts())

        else:
            if predicate != ANY:
                pos = self.__pos
                if predicate in pos:
                    predicateDictionary = pos[predicate]
                    if object != ANY:
                        if object in predicateDictionary:
                            for s in predicateDictionary[object].keys():
                                yield (
                                 (
                                  s, predicate, object), self.__contexts())

                    else:
                        for o in predicateDictionary.keys():
                            for s in predicateDictionary[o].keys():
                                yield (
                                 (
                                  s, predicate, o), self.__contexts())

            if object != ANY:
                osp = self.__osp
                if object in osp:
                    objectDictionary = osp[object]
                    for s in objectDictionary.keys():
                        for p in objectDictionary[s].keys():
                            yield (
                             (
                              s, p, object), self.__contexts())

            spo = self.__spo
            for s in spo.keys():
                subjectDictionary = spo[s]
                for p in subjectDictionary.keys():
                    for o in subjectDictionary[p].keys():
                        yield (
                         (
                          s, p, o), self.__contexts())

    def __len__(self, context=None):
        i = 0
        for triple in self.triples((None, None, None)):
            i += 1

        return i

    def bind(self, prefix, namespace):
        self.__prefix[namespace] = prefix
        self.__namespace[prefix] = namespace

    def unbind(self, prefix, namespace):
        del self.__prefix[namespace]
        del self.__namespace[prefix]

    def namespace(self, prefix):
        return self.__namespace.get(prefix, None)

    def prefix(self, namespace):
        return self.__prefix.get(namespace, None)

    def namespaces(self):
        for (prefix, namespace) in self.__namespace.iteritems():
            yield (prefix, namespace)

    def __contexts(self):
        if False:
            yield
        return