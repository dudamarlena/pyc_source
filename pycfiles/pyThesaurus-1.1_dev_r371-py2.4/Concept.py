# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyThesaurus/Concept.py
# Compiled at: 2008-10-06 10:31:21
from config import *

class Concept:
    __module__ = __name__

    def __init__(self, et=None, ht=None, net=None, bt=None, nt=None, st=None, rt=None, pubn=None, privn=None, contexts=None, TDict=dict, TList=list):
        """
                Create a new concept object.
                """
        self._dict = TDict
        self._list = TList
        self._et = et or self._list()
        self._ht = ht or self._list()
        self._net = net or self._list()
        self._bt = bt or self._list()
        self._nt = nt or self._list()
        self._st = st or self._list()
        self._rt = rt or self._list()
        self._pubn = pubn or self._dict()
        self._privn = privn or self._dict()
        self._contexts = contexts or self._list()

    def contexts(self):
        """
                """
        return self._contexts

    def could_be_joined_to(self, other_concept, M=matrix_comparation, S=minimum_score):
        """
                could_be_joined_to(object, object, M=list<list<int>>, S=int) -> bool

                Returns true if self is similar to other_concept using a matrix comparation M and a minimum score S.
                """
        if self.has_equivalents_terms(other_concept):
            s = 0
            for rel1 in range(len(relations)):
                for rel2 in range(len(relations)):
                    for t in self[relations[rel1]]:
                        if t in other_concept[relations[rel2]]:
                            s += M[rel1][rel2]

            similar = s > minimum_score
        else:
            similar = False
        return similar

    def join_to(self, other_concept, R=relations_precedence):
        """
                Join this concept to other_concept considering relations_precedence list R.
                """
        new_concept = Concept()
        for rel1 in range(len(relations)):
            for t in self[relations[rel1]]:
                otherRel = None
                for rel2 in range(len(relations)):
                    if t in other_concept[relations[rel2]]:
                        otherRel = rel2

                if otherRel is not None and otherRel is not rel1:
                    addAt = relation_more_precedent(rel1, otherRel, R)
                else:
                    addAt = rel1
                new_concept[addAt] = new_concept[addAt] + [t]

        return new_concept

    def has_equivalents_terms(self, other_concept):
        """
                Returns True if both concepts have a term in common.
                """
        equiv = False
        for t in self._et:
            if t in other_concept._et:
                equiv = True

        return equiv

    def relation_more_precedent(relation1, relation2, R):
        """
                Returns relation1 if it is more precedent than relation2, else it returns relation2.
                """
        if R.index(relation1) < R.index(relation2):
            rel = relation1
        else:
            rel = relation2
        return rel

    def __getitem__(self, rel):
        """
                Returns terms related to the concept in rel relationship.
                """
        if rel == '=':
            terms = self._et
        elif rel == '!':
            terms = self._net
        elif rel == '<':
            terms = self._bt
        elif rel == '>':
            terms = self._nt
        elif rel == '~':
            terms = self._st
        elif rel == '-':
            terms = self._rt
        elif rel == '#':
            terms = self._ht
        elif rel == '0':
            terms = self.get_prefered()
        else:
            raise KeyError, 'Relationship not defined'
        return terms

    def __setitem__(self, rel, terms):
        """
                Set terms related to the concept in rel relationship.
                """
        if rel == '=':
            self._et = terms
        elif rel == '!':
            self._net = terms
        elif rel == '<':
            self._bt = terms
        elif rel == '>':
            self._nt = terms
        elif rel == '~':
            self._st = terms
        elif rel == '-':
            self._rt = terms
        elif rel == '#':
            self._ht = terms
        elif rel == '0':
            self.set_prefered(terms)
        else:
            raise KeyError, 'Relationship not defined'

    def get_prefered(self, lang=[]):
        """
                get_prefered(object, str, list<str>) -> list<str>

                Return prefered terms of term t in all languages in lang. If lang is [] return all terms.
                """
        ls = []
        ts = []
        for tl in self._et:
            (t, l) = tl.split('@')
            if l not in ls and l in lang:
                ts.append(tl)
                ls.append(l)

        return ts

    def set_prefered(self, t):
        """
                set_prefered(object, str) -> None

                Set the prefered term t in some language
                """
        if t not in self._et:
            raise NoTermInConcept
        self._et.remove(t)
        self._et = [t] + self._et
        return

    def match(self, reg):
        """
                match(object, str) -> Bool

                Returns True if any equivalent term matchs reg.
                """
        return self._any_match(self['='], reg)

    def prefered_terms_match(self, reg, lang):
        """
                prefered_terms_match(object, str) -> Bool

                Returns True if any prefered term matchs reg.
                """
        return self._any_match(self.get_prefered(lang), reg)

    def prefered_terms_start_with(self, reg, lang):
        """
                prefered_terms_match(object, str) -> Bool

                Returns True if any prefered term starts with reg.
                """
        return self._any_starts_with(self.get_prefered(lang), reg)

    def _any_match(self, ts, reg):
        for term in ts:
            if reg.search(term):
                return True

        return False

    def _any_starts_with(self, ts, reg):
        for term in ts:
            if reg.match(term):
                return True

        return False