# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/iomemory.py
# Compiled at: 2008-04-06 18:54:11
"""An in-memory store plugin for `rdf`.

This is a plugin for rdf.plugins.stores package. See::

    http://pypi.python.org/pypi/rdf/ 

for more information on the Python rdf package.

TODO: example usage.

"""
__version__ = '0.9a1'
from rdf.term import BNode
from rdf.store import Store
Any = None

class IOMemory(Store):
    """    An integer-key-optimized-context-aware-in-memory store.

    Uses nested dictionaries to store triples and context. Each triple
    is stored in six such indices as follows cspo[c][s][p][o] = 1
    and cpos[c][p][o][s] = 1 and cosp[c][o][s][p] = 1 as well as
    spo[s][p][o] = [c] and pos[p][o][s] = [c] and pos[o][s][p] = [c]

    Context information is used to track the 'source' of the triple
    data for merging, unmerging, remerging purposes.  context aware
    store stores consume more memory size than non context stores.

    """
    context_aware = True
    formula_aware = True

    def __init__(self, configuration=None, identifier=None):
        super(IOMemory, self).__init__()
        self.cspo = self.createIndex()
        self.cpos = self.createIndex()
        self.cosp = self.createIndex()
        self.spo = self.createIndex()
        self.pos = self.createIndex()
        self.osp = self.createIndex()
        self.forward = self.createForward()
        self.reverse = self.createReverse()
        self.identifier = identifier or BNode()
        self.__namespace = self.createPrefixMap()
        self.__prefix = self.createPrefixMap()

    def bind(self, prefix, namespace):
        self.__prefix[namespace] = prefix
        self.__namespace[prefix] = namespace

    def namespace(self, prefix):
        return self.__namespace.get(prefix, None)

    def prefix(self, namespace):
        return self.__prefix.get(namespace, None)

    def namespaces(self):
        for (prefix, namespace) in self.__namespace.iteritems():
            yield (prefix, namespace)

    def defaultContext(self):
        return self.default_context

    def addContext(self, context):
        """ Add context w/o adding statement. Dan you can remove this if you want """
        if not self.reverse.has_key(context):
            ci = randid()
            while not self.forward.insert(ci, context):
                ci = randid()

            self.reverse[context] = ci

    def intToIdentifier(self, (si, pi, oi)):
        """ Resolve an integer triple into identifers. """
        return (
         self.forward[si], self.forward[pi], self.forward[oi])

    def identifierToInt(self, (s, p, o)):
        """ Resolve an identifier triple into integers. """
        return (
         self.reverse[s], self.reverse[p], self.reverse[o])

    def uniqueSubjects(self, context=None):
        if context is None:
            index = self.spo
        else:
            index = self.cspo[context]
        for si in index.keys():
            yield self.forward[si]

        return

    def uniquePredicates(self, context=None):
        if context is None:
            index = self.pos
        else:
            index = self.cpos[context]
        for pi in index.keys():
            yield self.forward[pi]

        return

    def uniqueObjects(self, context=None):
        if context is None:
            index = self.osp
        else:
            index = self.cosp[context]
        for oi in index.keys():
            yield self.forward[oi]

        return

    def createForward(self):
        return {}

    def createReverse(self):
        return {}

    def createIndex(self):
        return {}

    def createPrefixMap(self):
        return {}

    def add(self, triple, context, quoted=False):
        """        Add a triple to the store.
        """
        Store.add(self, triple, context, quoted)
        for (triple, cg) in self.triples(triple, context):
            return

        (subject, predicate, object) = triple
        f = self.forward
        r = self.reverse
        if not r.has_key(subject):
            si = randid()
            while f.has_key(si):
                si = randid()

            f[si] = subject
            r[subject] = si
        else:
            si = r[subject]
        if not r.has_key(predicate):
            pi = randid()
            while f.has_key(pi):
                pi = randid()

            f[pi] = predicate
            r[predicate] = pi
        else:
            pi = r[predicate]
        if not r.has_key(object):
            oi = randid()
            while f.has_key(oi):
                oi = randid()

            f[oi] = object
            r[object] = oi
        else:
            oi = r[object]
        if not r.has_key(context):
            ci = randid()
            while f.has_key(ci):
                ci = randid()

            f[ci] = context
            r[context] = ci
        else:
            ci = r[context]
        self._setNestedIndex(self.cspo, ci, si, pi, oi)
        self._setNestedIndex(self.cpos, ci, pi, oi, si)
        self._setNestedIndex(self.cosp, ci, oi, si, pi)
        if not quoted:
            self._setNestedIndex(self.spo, si, pi, oi, ci)
            self._setNestedIndex(self.pos, pi, oi, si, ci)
            self._setNestedIndex(self.osp, oi, si, pi, ci)

    def _setNestedIndex(self, index, *keys):
        for key in keys[:-1]:
            if not index.has_key(key):
                index[key] = self.createIndex()
            index = index[key]

        index[keys[(-1)]] = 1

    def _removeNestedIndex(self, index, *keys):
        """ Remove context from the list of contexts in a nested index.

        Afterwards, recursively remove nested indexes when they became empty.
        """
        parents = []
        for key in keys[:-1]:
            parents.append(index)
            index = index[key]

        del index[keys[(-1)]]
        n = len(parents)
        for i in xrange(n):
            index = parents[(n - 1 - i)]
            key = keys[(n - 1 - i)]
            if len(index[key]) == 0:
                del index[key]

    def remove(self, triple, context=None):
        Store.remove(self, triple, context)
        if context is not None:
            if context == self:
                context = None
        f = self.forward
        r = self.reverse
        if context is None:
            for (triple, cg) in self.triples(triple):
                (subject, predicate, object) = triple
                (si, pi, oi) = self.identifierToInt((subject, predicate, object))
                contexts = list(self.contexts(triple))
                for context in contexts:
                    ci = r[context]
                    del self.cspo[ci][si][pi][oi]
                    del self.cpos[ci][pi][oi][si]
                    del self.cosp[ci][oi][si][pi]
                    self._removeNestedIndex(self.spo, si, pi, oi, ci)
                    self._removeNestedIndex(self.pos, pi, oi, si, ci)
                    self._removeNestedIndex(self.osp, oi, si, pi, ci)

        else:
            (subject, predicate, object) = triple
            ci = r.get(context, None)
            if ci:
                for (triple, cg) in self.triples(triple, context):
                    (si, pi, oi) = self.identifierToInt(triple)
                    del self.cspo[ci][si][pi][oi]
                    del self.cpos[ci][pi][oi][si]
                    del self.cosp[ci][oi][si][pi]
                    try:
                        self._removeNestedIndex(self.spo, si, pi, oi, ci)
                        self._removeNestedIndex(self.pos, pi, oi, si, ci)
                        self._removeNestedIndex(self.osp, oi, si, pi, ci)
                    except KeyError:
                        pass

        if subject is None and predicate is None and object is None:
            try:
                ci = self.reverse[context]
                del self.cspo[ci]
                del self.cpos[ci]
                del self.cosp[ci]
            except KeyError:
                pass

        return

    def triples(self, triple, context=None):
        """A generator over all the triples matching """
        if context is not None:
            if context == self:
                context = None
        (subject, predicate, object) = triple
        ci = si = pi = oi = Any
        if context is None:
            spo = self.spo
            pos = self.pos
            osp = self.osp
        else:
            try:
                ci = self.reverse[context]
                spo = self.cspo[ci]
                pos = self.cpos[ci]
                osp = self.cosp[ci]
            except KeyError:
                return

            try:
                if subject is not Any:
                    si = self.reverse[subject]
                if predicate is not Any:
                    pi = self.reverse[predicate]
                if object is not Any:
                    oi = self.reverse[object]
            except KeyError, e:
                return

        if si != Any:
            if spo.has_key(si):
                subjectDictionary = spo[si]
                if pi != Any:
                    if subjectDictionary.has_key(pi):
                        if oi != Any:
                            if subjectDictionary[pi].has_key(oi):
                                (ss, pp, oo) = self.intToIdentifier((si, pi, oi))
                                yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))
                        else:
                            for o in subjectDictionary[pi].keys():
                                (ss, pp, oo) = self.intToIdentifier((si, pi, o))
                                yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))

                else:
                    for p in subjectDictionary.keys():
                        if oi != Any:
                            if subjectDictionary[p].has_key(oi):
                                (ss, pp, oo) = self.intToIdentifier((si, p, oi))
                                yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))
                        else:
                            for o in subjectDictionary[p].keys():
                                (ss, pp, oo) = self.intToIdentifier((si, p, o))
                                yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))

        if pi != Any:
            if pos.has_key(pi):
                predicateDictionary = pos[pi]
                if oi != Any:
                    if predicateDictionary.has_key(oi):
                        for s in predicateDictionary[oi].keys():
                            (ss, pp, oo) = self.intToIdentifier((s, pi, oi))
                            yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))

                else:
                    for o in predicateDictionary.keys():
                        for s in predicateDictionary[o].keys():
                            (ss, pp, oo) = self.intToIdentifier((s, pi, o))
                            yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))

        if oi != Any:
            if osp.has_key(oi):
                objectDictionary = osp[oi]
                for s in objectDictionary.keys():
                    for p in objectDictionary[s].keys():
                        (ss, pp, oo) = self.intToIdentifier((s, p, oi))
                        yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))

        for s in spo.keys():
            subjectDictionary = spo[s]
            for p in subjectDictionary.keys():
                for o in subjectDictionary[p].keys():
                    (ss, pp, oo) = self.intToIdentifier((s, p, o))
                    yield ((ss, pp, oo), (c for c in self.contexts((ss, pp, oo))))

        return

    def __len__(self, context=None):
        if context is not None:
            if context == self:
                context = None
        count = 0
        for (triple, cg) in self.triples((Any, Any, Any), context):
            count += 1

        return count

    def contexts(self, triple=None):
        if triple:
            (si, pi, oi) = self.identifierToInt(triple)
            for ci in self.spo[si][pi][oi]:
                yield self.forward[ci]

        for ci in self.cspo.keys():
            yield self.forward[ci]


import random

def randid(randint=random.randint, choice=random.choice, signs=(-1, 1)):
    return choice(signs) * randint(1, 2000000000)


del random