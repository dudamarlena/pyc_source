# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grimnes/projects/rdflib/rdfextras/rdfextras/store/REGEXMatching.py
# Compiled at: 2012-04-24 09:28:08
"""
This wrapper intercepts calls through the store interface which make use of
The REGEXTerm class to represent matches by REGEX instead of literal
comparison Implemented for stores that don't support this and essentially
provides the support by replacing the REGEXTerms by wildcards (None) and
matching against the results from the store its wrapping
"""
from rdflib.store import Store
from rdflib.graph import Graph
import re
NATIVE_REGEX = 0
PYTHON_REGEX = 1

class REGEXTerm(unicode):
    """
    REGEXTerm can be used in any term slot and is interpreted as a request to
    perform a REGEX match (not a string comparison) using the value
    (pre-compiled) for checking rdf:type matches
    """

    def __init__(self, expr):
        self.compiledExpr = re.compile(expr)

    def __reduce__(self):
        return (
         REGEXTerm, (unicode(''),))


def regexCompareQuad(quad, regexQuad):
    for index in range(4):
        if isinstance(regexQuad[index], REGEXTerm) and not regexQuad[index].compiledExpr.match(quad[index]):
            return False

    return True


class REGEXMatching(Store):

    def __init__(self, storage):
        self.storage = storage
        self.context_aware = storage.context_aware
        self.formula_aware = storage.formula_aware
        self.transaction_aware = storage.transaction_aware

    def open(self, configuration, create=True):
        return self.storage.open(configuration, create)

    def close(self, commit_pending_transaction=False):
        self.storage.close()

    def destroy(self, configuration):
        self.storage.destroy(configuration)

    def add(self, triple, context, quoted=False):
        subject, predicate, object_ = triple
        self.storage.add((subject, predicate, object_), context, quoted)

    def remove(self, triple, context=None):
        subject, predicate, object_ = triple
        if isinstance(subject, REGEXTerm) or isinstance(predicate, REGEXTerm) or isinstance(object_, REGEXTerm) or context is not None and isinstance(context.identifier, REGEXTerm):
            s = not isinstance(subject, REGEXTerm) and subject or None
            p = not isinstance(predicate, REGEXTerm) and predicate or None
            o = not isinstance(object_, REGEXTerm) and object_ or None
            c = context is not None and not isinstance(context.identifier, REGEXTerm) and context or None
            removeQuadList = []
            for (s1, p1, o1), cg in self.storage.triples((s, p, o), c):
                for ctx in cg:
                    ctx = ctx.identifier
                    if regexCompareQuad((
                     s1, p1, o1, ctx), (
                     subject, predicate, object_,
                     context is not None and context.identifier or context)):
                        removeQuadList.append((s1, p1, o1, ctx))

            for s, p, o, c in removeQuadList:
                self.storage.remove((s, p, o), c and Graph(self, c) or c)

        else:
            self.storage.remove((subject, predicate, object_), context)
        return

    def triples(self, triple, context=None):
        subject, predicate, object_ = triple
        if isinstance(subject, REGEXTerm) or isinstance(predicate, REGEXTerm) or isinstance(object_, REGEXTerm) or context is not None and isinstance(context.identifier, REGEXTerm):
            s = not isinstance(subject, REGEXTerm) and subject or None
            p = not isinstance(predicate, REGEXTerm) and predicate or None
            o = not isinstance(object_, REGEXTerm) and object_ or None
            c = context is not None and not isinstance(context.identifier, REGEXTerm) and context or None
            for (s1, p1, o1), cg in self.storage.triples((s, p, o), c):
                matchingCtxs = []
                for ctx in cg:
                    if c is None:
                        if context is None or context.identifier.compiledExpr.match(ctx.identifier):
                            matchingCtxs.append(ctx)
                    else:
                        matchingCtxs.append(ctx)

                if matchingCtxs and regexCompareQuad((
                 s1, p1, o1, None), (subject, predicate, object_, None)):
                    yield (
                     (
                      s1, p1, o1), (c for c in matchingCtxs))

        else:
            for (s1, p1, o1), cg in self.storage.triples((
             subject, predicate, object_), context):
                yield (
                 (
                  s1, p1, o1), cg)

        return

    def __len__(self, context=None):
        return self.storage.__len__(context)

    def contexts(self, triple=None):
        for ctx in self.storage.contexts(triple):
            yield ctx

    def remove_context(self, identifier):
        self.storage.remove((None, None, None), identifier)
        return

    def bind(self, prefix, namespace):
        self.storage.bind(prefix, namespace)

    def prefix(self, namespace):
        return self.storage.prefix(namespace)

    def namespace(self, prefix):
        return self.storage.namespace(prefix)

    def namespaces(self):
        return self.storage.namespaces()

    def commit(self):
        self.storage.commit()

    def rollback(self):
        self.storage.rollback()