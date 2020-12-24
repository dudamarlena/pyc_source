# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/MeterSlot.py
# Compiled at: 2019-06-02 18:11:38
from entity import entity

class MeterSlot(entity):

    def __init__(self, i, unit, token, wordpos, word, i_word=0, i_syll_in_word=0, wordtoken=None, meter=None):
        self.i = i
        self.children = [unit]
        self.token = token
        self.featpaths = {}
        self.wordpos = wordpos
        self.word = word
        self.issplit = False
        self.i_word = i_word
        self.i_syll_in_word = i_syll_in_word
        self.wordtoken = wordtoken
        self.meter = meter
        self.feat('prom.stress', unit.feature('prom.stress'))
        self.feat('prom.strength', unit.feature('prom.strength'))
        self.feat('prom.kalevala', unit.feature('prom.kalevala'))
        self.feat('prom.weight', unit.children[0].feature('prom.weight'))
        self.feat('shape', unit.str_shape())
        self.feat('prom.vheight', unit.children[0].feature('prom.vheight'))
        self.feat('word.polysyll', self.word.numSyll > 1)
        self.feat('prom.phrasal_stress', self.phrasal_stress)
        self.feat('prom.phrasal_strength', self.phrasal_strength)
        self.feat('prom.phrasal_head', self.phrasal_head)

    @property
    def phrasal_strength(self):
        if not self.wordtoken:
            return
        else:
            if self.word.numSyll > 1 and self.stress != 'P':
                return
            if self.wordtoken.feats.get('phrasal_stress_peak', ''):
                return True
            if self.wordtoken.feats.get('phrasal_stress_valley', ''):
                return False
            return

    @property
    def phrasal_head(self):
        if not self.wordtoken:
            return
        else:
            if self.word.numSyll > 1 and self.stress != 'P':
                return
            if self.wordtoken.feats.get('phrasal_head', ''):
                return True
            return

    @property
    def phrasal_stress(self):
        if not self.wordtoken:
            return
        else:
            if self.word.numSyll > 1 and self.stress != 'P':
                return
            else:
                if self.meter.config.get('phrasal_stress_norm_context_is_sentence', 0):
                    return self.wordtoken.phrasal_stress
                return self.wordtoken.phrasal_stress_line

            return

    def str_meter(self):
        return self.meter

    def str_token(self):
        if not hasattr(self, 'meter'):
            return self.token
        else:
            if self.meter == 's':
                return self.token.upper()
            return self.token.lower()

    @property
    def stress(self):
        if self.feature('prom.stress') == 1.0:
            return 'P'
        if self.feature('prom.stress') == 0.5:
            return 'S'
        if self.feature('prom.stress') == 0.0:
            return 'U'