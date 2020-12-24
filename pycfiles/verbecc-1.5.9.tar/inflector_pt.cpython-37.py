# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\inflector_pt.py
# Compiled at: 2019-07-28 18:46:02
# Size of source mod 2**32: 4163 bytes
from verbecc import inflector

class InflectorPt(inflector.Inflector):

    def __init__(self):
        self.lang = 'pt'
        super(InflectorPt, self).__init__()

    def _add_subjunctive_relative_pronoun(self, s, tense_name):
        if tense_name == 'presente':
            return 'que ' + s
        if tense_name == 'pretérito-imperfeito':
            return 'se ' + s
        if tense_name == 'futuro':
            return 'quando ' + s
        return s

    def _add_adverb_if_applicable(self, s, mood_name, tense_name):
        if mood_name == 'imperativo':
            if tense_name == 'negativo':
                return 'não ' + s
        if mood_name == 'infinitivo':
            if tense_name == 'infinitivo-pessoal-presente':
                return 'por ' + s
        return s

    def _add_reflexive_pronoun_or_pronoun_suffix_if_applicable(self, s, is_reflexive, mood_name, tense_name, person):
        imperative = mood_name == 'imperativo'
        if (imperative or mood_name) == 'infinitivo':
            if tense_name == 'infinitivo-pessoal-presente':
                s += ' ' + self._get_pronoun_suffix(person, imperative=imperative)
        return s

    def _get_default_pronoun(self, person, gender='m', is_reflexive=False):
        ret = ''
        if person == '1s':
            ret = 'eu'
            if is_reflexive:
                ret += ' me'
        elif person == '2s':
            ret = 'tu'
            if is_reflexive:
                ret += ' te'
        elif person == '3s':
            ret = 'ele'
            if gender == 'f':
                ret = 'ela'
            if is_reflexive:
                ret += ' se'
        elif person == '1p':
            ret = 'nós'
            if is_reflexive:
                ret += ' nos'
        elif person == '2p':
            ret = 'vós'
            if is_reflexive:
                ret += ' se'
        elif person == '3p':
            ret = 'eles'
            if gender == 'f':
                ret = 'elas'
            if is_reflexive:
                ret += ' se'
        return ret

    def _get_pronoun_suffix(self, person, gender='m', imperative=True):
        ret = ''
        if person == '1s':
            ret = 'eu'
        if person == '2s':
            ret = 'tu'
        else:
            if person == '3s':
                ret = 'você'
                ret = imperative or 'ele'
            else:
                if person == '1p':
                    ret = 'nós'
                else:
                    if person == '2p':
                        ret = 'vós'
                    else:
                        if person == '3p':
                            ret = 'vocês'
                            if not imperative:
                                ret = 'eles'
        return ret

    def _get_tenses_conjugated_without_pronouns(self):
        return [
         'particípio',
         'infinitivo',
         'infinitivo-pessoal-presente', 'infinitivo-pessoal-composto',
         'afirmativo', 'negativo',
         'gerúndio']

    def _get_auxilary_verb(self, co, mood_name, tense_name):
        return 'ter'

    def _get_subjunctive_mood_name(self):
        return 'subjuntivo'

    def _get_participle_mood_name(self):
        return 'particípio'

    def _get_participle_tense_name(self):
        return 'particípio'

    def _get_compound_conjugations_hv_map(self):
        return {'indicativo':{'pretérito-perfeito-composto':'presente', 
          'pretérito-mais-que-perfeito-composto':'pretérito-imperfeito', 
          'pretérito-mais-que-perfeito-anterior':'pretérito-mais-que-perfeito', 
          'futuro-do-presente-composto':'futuro-do-presente'}, 
         'subjuntivo':{'pretérito-perfeito':'presente', 
          'pretérito-mais-que-perfeito':'pretérito-imperfeito', 
          'futuro-composto':'futuro'}, 
         'condicional':{'futuro-do-pretérito-composto': 'futuro-do-pretérito'}, 
         'infinitivo':{'infinitivo-pessoal-composto': 'infinitivo-pessoal-presente'}}