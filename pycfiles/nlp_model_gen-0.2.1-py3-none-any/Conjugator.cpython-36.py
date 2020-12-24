# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/Conjugator.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 10825 bytes
import fnmatch, copy
from terminaltables import AsciiTable
from .helpers.presenteIndicativoHelper import presente_conj
from .helpers.preteritoPerfSimpleHelper import preterito_perf_simple_conj
from .helpers.preteritoImperfHelper import preterito_imperf_conj
from .helpers.futuroSimpleHelper import futuro_simple_conj
from .helpers.condicionalSimpleAHelper import condicional_simple_A_conj
from .helpers.condicionalSimpleBHelper import condicional_simple_B_conj
from .helpers.imperativoAHelper import imperativo_A_conj
from .helpers.imperativoBHelper import imperativo_B_conj
from .helpers.imperativoCHelper import imperativo_C_conj
from .helpers.participioHelper import participio
from .helpers.gerundioHelper import gerundio
from .helpers.irregularVerbGeneratorHelper import get_irregular_verbs

class Conjugator:

    def __init__(self, mode, general_config, irregular_verb_groups_config, irregular_verb_exceptions_config):
        self._Conjugator__mode = mode
        self._Conjugator__configs = {'config':general_config, 
         'irregular_verb_exceptions':{},  'irregular_verb_groups':irregular_verb_groups_config, 
         'irregular_verb_exceptions_config':irregular_verb_exceptions_config}
        get_irregular_verbs(self._Conjugator__configs['irregular_verb_exceptions'], self._Conjugator__mode, self._Conjugator__configs)

    def set_mode(self, mode):
        self._Conjugator__mode = mode

    def set_general_config(self, general_config):
        self._Conjugator__configs['config'] = general_config
        self._Conjugator__configs['irregular_verb_exceptions'] = {}
        get_irregular_verbs(self._Conjugator__configs['irregular_verb_exceptions'], self._Conjugator__mode, self._Conjugator__configs)

    def set_irregular_verb_groups_config(self, irregular_verb_groups_config):
        self._Conjugator__configs['irregular_verb_groups'] = irregular_verb_groups_config
        self._Conjugator__configs['irregular_verb_exceptions'] = {}
        get_irregular_verbs(self._Conjugator__configs['irregular_verb_exceptions'], self._Conjugator__mode, self._Conjugator__configs)

    def set_irregular_verb_exceptions_config(self, irregular_verb_exceptions_config):
        self._Conjugator__configs['irregular_verb_exceptions_config'] = irregular_verb_exceptions_config
        self._Conjugator__configs['irregular_verb_exceptions'] = {}
        get_irregular_verbs(self._Conjugator__configs['irregular_verb_exceptions'], self._Conjugator__mode, self._Conjugator__configs)

    def __apply_conjugation(self, verb, conjugation):
        return conjugation(verb, False, self._Conjugator__mode, self._Conjugator__configs)

    def generar_conjugaciones(self, verb):
        return {'inf':[
          verb], 
         'ger':self._Conjugator__apply_conjugation(verb, gerundio), 
         'part':self._Conjugator__apply_conjugation(verb, participio), 
         'pres':self._Conjugator__apply_conjugation(verb, presente_conj), 
         'pret_perf':self._Conjugator__apply_conjugation(verb, preterito_perf_simple_conj), 
         'pret_imperf':self._Conjugator__apply_conjugation(verb, preterito_imperf_conj), 
         'fut':self._Conjugator__apply_conjugation(verb, futuro_simple_conj), 
         'impA':self._Conjugator__apply_conjugation(verb, imperativo_A_conj), 
         'impB':self._Conjugator__apply_conjugation(verb, imperativo_B_conj), 
         'impC':self._Conjugator__apply_conjugation(verb, imperativo_C_conj), 
         'condA':self._Conjugator__apply_conjugation(verb, condicional_simple_A_conj), 
         'condB':self._Conjugator__apply_conjugation(verb, condicional_simple_B_conj)}

    def __generar_dict_irregular_concatenado(self, key, verb):
        if key == '':
            conjugation = copy.deepcopy(self._Conjugator__configs['irregular_verb_exceptions'][verb])
            base_verb = ''
        else:
            conjugation = copy.deepcopy(self._Conjugator__configs['irregular_verb_exceptions'][key])
            base_verb = verb.replace(key, '')
        for key in conjugation.keys():
            i = 0
            while i < len(conjugation[key]):
                if conjugation[key][i] != '':
                    conjugation[key][i] = base_verb + conjugation[key][i]
                i += 1

        return conjugation

    def __generar_diccionario_conjugacion(self, verb):
        if not any(fnmatch.fnmatch(verb, suffix) for suffix in self._Conjugator__configs['config']['verb_suffixes']):
            return {}
        else:
            key = self._Conjugator__extract_key(verb)
            if key is not None:
                return self._Conjugator__generar_dict_irregular_concatenado(key, verb)
            return self.generar_conjugaciones(verb)

    def __extract_key(self, verb):
        for key in self._Conjugator__configs['irregular_verb_exceptions']:
            if fnmatch.fnmatch(verb, '*' + key):
                if key not in self._Conjugator__configs['config']['irregular_suffix_exceptions']:
                    if key != verb:
                        return key
                    else:
                        return ''

    def __empty_dict(self):
        return self._Conjugator__configs['config']['empty_conj_dict']

    def __contruir_primera_fila(self, conjugation):
        return [
         self._Conjugator__configs['config']['table_headers'][0],
         [
          self._Conjugator__configs['config']['row_headers'][0][0], conjugation['pres'][0], conjugation['pret_imperf'][0], conjugation['pret_perf'][0], conjugation['condA'][0]],
         [
          self._Conjugator__configs['config']['row_headers'][0][1], conjugation['pres'][1], conjugation['pret_imperf'][1], conjugation['pret_perf'][1], conjugation['condA'][1]],
         [
          self._Conjugator__configs['config']['row_headers'][0][2], conjugation['pres'][2], conjugation['pret_imperf'][2], conjugation['pret_perf'][2], conjugation['condA'][2]],
         [
          self._Conjugator__configs['config']['row_headers'][0][3], conjugation['pres'][3], conjugation['pret_imperf'][3], conjugation['pret_perf'][3], conjugation['condA'][3]],
         [
          self._Conjugator__configs['config']['row_headers'][0][4], conjugation['pres'][4], conjugation['pret_imperf'][4], conjugation['pret_perf'][4], conjugation['condA'][4]],
         [
          self._Conjugator__configs['config']['row_headers'][0][5], conjugation['pres'][5], conjugation['pret_imperf'][5], conjugation['pret_perf'][5], conjugation['condA'][5]]]

    def __construir_segunda_fila(self, conjugation):
        return [
         self._Conjugator__configs['config']['table_headers'][1],
         [
          self._Conjugator__configs['config']['row_headers'][0][0], conjugation['fut'][0], conjugation['condB'][0], conjugation['impA'][0], conjugation['impB'][0], conjugation['impC'][0]],
         [
          self._Conjugator__configs['config']['row_headers'][0][1], conjugation['fut'][1], conjugation['condB'][1], conjugation['impA'][1], conjugation['impB'][1], conjugation['impC'][1]],
         [
          self._Conjugator__configs['config']['row_headers'][0][2], conjugation['fut'][2], conjugation['condB'][2], conjugation['impA'][2], conjugation['impB'][2], conjugation['impC'][2]],
         [
          self._Conjugator__configs['config']['row_headers'][0][3], conjugation['fut'][3], conjugation['condB'][3], conjugation['impA'][3], conjugation['impB'][3], conjugation['impC'][3]],
         [
          self._Conjugator__configs['config']['row_headers'][0][4], conjugation['fut'][4], conjugation['condB'][4], conjugation['impA'][4], conjugation['impB'][4], conjugation['impC'][4]],
         [
          self._Conjugator__configs['config']['row_headers'][0][5], conjugation['fut'][5], conjugation['condB'][5], conjugation['impA'][5], conjugation['impB'][5], conjugation['impC'][5]]]

    def __construir_tercera_fila(self, conjugation):
        return [
         self._Conjugator__configs['config']['table_headers'][2],
         [
          self._Conjugator__configs['config']['row_headers'][1][0], conjugation['inf'][0]],
         [
          self._Conjugator__configs['config']['row_headers'][1][1], conjugation['ger'][0]],
         [
          self._Conjugator__configs['config']['row_headers'][1][2], conjugation['part'][0]],
         [
          self._Conjugator__configs['config']['row_headers'][1][3], conjugation['part'][1]],
         [
          self._Conjugator__configs['config']['row_headers'][1][4], conjugation['part'][2]]]

    def table_view(self, verb):
        conjugation = self._Conjugator__generar_diccionario_conjugacion(verb)
        if conjugation == {}:
            conjugation = self._Conjugator__empty_dict()
        table_data_1 = self._Conjugator__contruir_primera_fila(conjugation)
        table_01 = AsciiTable(table_data_1)
        table_data_2 = self._Conjugator__construir_segunda_fila(conjugation)
        table_02 = AsciiTable(table_data_2)
        table_data_3 = self._Conjugator__construir_tercera_fila(conjugation)
        table_03 = AsciiTable(table_data_3)
        print(table_03.table)
        print('')
        print(table_01.table)
        print('')
        print(table_02.table)