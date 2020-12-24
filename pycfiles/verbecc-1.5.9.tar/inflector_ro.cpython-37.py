# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\inflector_ro.py
# Compiled at: 2019-07-28 18:47:17
# Size of source mod 2**32: 2214 bytes
from verbecc import inflector

class InflectorRo(inflector.Inflector):

    def __init__(self):
        self.lang = 'ro'
        super(InflectorRo, self).__init__()

    def _add_adverb_if_applicable(self, s, mood_name, tense_name):
        if mood_name == 'imperativ':
            if tense_name == 'negativ':
                return 'nu ' + s
        return s

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'eu'
            if is_reflexive:
                ret += ' mă'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'el'
            if gender == 'f':
                ret = 'ea'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'noi'
            if is_reflexive:
                ret += ' ne'
        elif person == '2p':
            ret = 'voi'
            if is_reflexive:
                ret += ' vă'
        elif person == '3p':
            ret = 'ei'
            if gender == 'f':
                ret = 'ele'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return [
         'participiu',
         'afirmativ',
         'imperativ', 'negativ',
         'gerunziu']

    def _get_auxilary_verb(self, co, mood_name, tense_name):
        if tense_name == 'viitor-1':
            return 'voi'
        return 'avea'

    def _get_subjunctive_mood_name(self):
        return 'conjunctiv'

    def _get_participle_mood_name(self):
        return 'participiu'

    def _get_participle_tense_name(self):
        return 'participiu'

    def _get_compound_conjugations_hv_map(self):
        return {'indicativ': {'perfect-compus': 'prezent'}}