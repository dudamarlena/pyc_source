# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ryan/DH/prosodic/lib/WordToken.py
# Compiled at: 2019-06-07 00:03:27
from entity import entity, being

class WordToken(entity):

    def __init__(self, words, token, is_punct=False, sentence=None, line=None):
        self.children = words
        self.token = token
        self.is_punct = is_punct
        self.sentence = None
        self.feats = {}
        self.line = line
        return

    def __getitem__(self, key):
        return self.children[key]

    def __repr__(self):
        return '<' + self.classname() + ':' + self.u2s(self.token) + '>'

    def set_as_best_word_option(self, wordobj):
        if wordobj not in self.children:
            raise Exception("You're trying to prioritize this wordobj " + str(wordobj) + ', but it was never in this wordtoken ' + str(self) + ' to begin with!')
        if len(self.children) < 2:
            return
        self.children = list(self.children)
        self.children.remove(wordobj)
        self.children.insert(0, wordobj)

    def has_stressed_variant(self):
        return True in [ 'P' in word.stress for word in self.children ]

    def has_unstressed_variant(self):
        return True in [ 'P' not in word.stress for word in self.children ]

    def add_unstressed_variant(self):
        if not self.children:
            return
        wordobj = self.children[0]
        wordobj.feats['functionword'] = True
        self.children += [wordobj.get_unstressed_variant()]

    def add_stressed_variant(self, stress_pattern=None):
        if not self.children:
            return
        wordobj = self.children[0]
        new_wordobj = wordobj.get_stressed_variant(stress_pattern)
        if new_wordobj:
            self.children += [new_wordobj]

    def remove_unstressed_variant(self):
        new_wordobjs = []
        for wordobj in self.children:
            if 'P' not in wordobj.stress:
                continue
            new_wordobjs += [wordobj]

        self.children = new_wordobjs

    def remove_stressed_variant(self):
        new_wordobjs = []
        for wordobj in self.children:
            if 'P' in wordobj.stress:
                continue
            new_wordobjs += [wordobj]

        self.children = new_wordobjs

    def make_stress_ambiguous(self, stress_pattern=None):
        if not self.children:
            return
        if self.has_stressed_variant() and not self.has_unstressed_variant():
            self.add_unstressed_variant()
        elif self.has_unstressed_variant() and not self.has_stressed_variant():
            self.add_stressed_variant(stress_pattern=stress_pattern)

    def make_unstressed(self):
        if not self.children:
            return
        if not self.has_unstressed_variant():
            self.add_unstressed_variant()
        if self.has_stressed_variant():
            self.remove_stressed_variant()

    def make_stressed(self, stress_pattern=None):
        if not self.children:
            return
        if not self.has_stressed_variant():
            self.add_stressed_variant()
        if self.has_unstressed_variant():
            self.remove_unstressed_variant()

    @property
    def stress(self):
        if not self.children:
            return ''
        return self.children[0].stress

    @property
    def weight(self):
        if not self.children:
            return ''
        return self.children[0].weight

    @property
    def phrasal_stress(self):
        ps = self.feats.get('mean', None)
        if ps == None:
            return
        else:
            import numpy as np
            if np.isnan(ps):
                return
            return ps

    @property
    def phrasal_stress_line(self):
        ps = self.feats.get('mean_line', None)
        if ps == None:
            return
        else:
            import numpy as np
            if np.isnan(ps):
                return
            return ps

    @property
    def phrasal_stress_norm(self):
        ps = self.feats.get('norm_mean', None)
        if ps == None:
            return
        else:
            import numpy as np
            if np.isnan(ps):
                return
            return ps

    @property
    def phrasal_stress_norm_line(self):
        ps = self.feats.get('norm_mean_line', None)
        if ps == None:
            return
        else:
            import numpy as np
            if np.isnan(ps):
                return
            return ps