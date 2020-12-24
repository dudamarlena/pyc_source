# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/imperativoAHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 10297 bytes
import fnmatch
from .irregularVerbCastHelper import irregular_cast_group_01, irregular_cast_group_02, irregular_cast_group_03, irregular_cast_group_04_b, irregular_cast_group_06, irregular_cast_group_07, irregular_cast_group_08_a, irregular_cast_group_08_b, irregular_cast_group_09, irregular_cast_group_10, irregular_cast_group_11, irregular_cast_group_12_a, irregular_cast_group_12_b, irregular_cast_group_13_a

def imperativo_A_conj(verb, force_conj, mode, configs):
    irregular_verb_exceptions = configs['irregular_verb_exceptions']
    irregular_verb_groups = configs['irregular_verb_groups']
    config = configs['config']
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ('*ar', '*er', '*ir', '*ár',
                                                            '*ér', '*ír')):
        return ['', '', '', '', '', '']
    else:
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb) - 2]
        ncer_flag = False
        ger_gir_flag = False
        car_flag = False
        zar_flag = False
        guir_flag = False
        guar_flag = False
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                if fnmatch.fnmatch(verb, '*car'):
                    car_flag = True
                else:
                    if fnmatch.fnmatch(verb, '*zar'):
                        zar_flag = True
                    else:
                        if fnmatch.fnmatch(verb, '*guar'):
                            guar_flag = True
                        if fnmatch.fnmatch(verb, '*gar'):
                            suffix_conj = [
                             '', 'á', 'ue', 'uemos', 'ad', 'uen']
                        else:
                            suffix_conj = [
                             '', 'á', 'e', 'emos', 'ad', 'en']
                    if mode != 0:
                        suffix_conj[1] = 'a'
                    if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                        if fnmatch.fnmatch(verb, '*ncer'):
                            ncer_flag = True
                        if fnmatch.fnmatch(verb, '*ger'):
                            ger_gir_flag = True
                        suffix_conj = [
                         '', 'é', 'a', 'amos', 'ed', 'an']
                if fnmatch.fnmatch(verb, '*ir'):
                    if fnmatch.fnmatch(verb, '*gir'):
                        ger_gir_flag = True
                    if fnmatch.fnmatch(verb, '*guir'):
                        guir_flag = True
                    if mode == 0:
                        suffix_conj = [
                         '', 'í', 'a', 'amos', 'id', 'an']
                    else:
                        suffix_conj = [
                         '', 'e', 'a', 'amos', 'id', 'an']
                    if fnmatch.fnmatch(verb, '*ír'):
                        if fnmatch.fnmatch(verb, '*gír'):
                            ger_gir_flag = True
                        if fnmatch.fnmatch(verb, '*guír'):
                            guir_flag = True
                        if mode == 0:
                            suffix_conj = [
                             '', 'eí', 'ía', 'iamos', 'eíd', 'ían']
                        else:
                            suffix_conj = [
                             '', 'íe', 'ía', 'iamos', 'eíd', 'ían']
        else:
            return irregular_verb_exceptions[verb]['impA']
        verb_conj.append('')
        for i in range(1, 6):
            base_form = base_verb
            if i in config['singular'] and not mode == 0 or mode == 0 and i in config['singular'] and i not in config['segunda_persona'] or i in config['plural'] and i in config['tercera_persona']:
                base_form = irregular_cast_group_01(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_02(verb, base_form, irregular_verb_groups)
            if i not in config['segunda_persona']:
                base_form = irregular_cast_group_03(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_04_b(verb, base_form, irregular_verb_groups)
            if mode != 0 and not (i in config['segunda_persona'] and i in config['plural']) or i not in config['segunda_persona']:
                base_form = irregular_cast_group_06(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_07(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_10(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_11(verb, base_form, irregular_verb_groups)
            if not mode == 0 and (i in config['singular'] or i in config['tercera_persona']) or mode == 0 and (i in config['singular'] and i not in config['segunda_persona'] or i in config['tercera_persona']):
                base_form = irregular_cast_group_08_a(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_12_a(verb, base_form, irregular_verb_groups)
            if i in config['primera_persona']:
                if i in config['plural']:
                    base_form = irregular_cast_group_08_b(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_12_b(verb, base_form, irregular_verb_groups)
            if i in config['tercera_persona']:
                base_form = irregular_cast_group_09(verb, base_form, irregular_verb_groups)
            if i in config['primera_persona'] or i in config['tercera_persona']:
                if verb == 'delinquir':
                    base_form.replace('qu', 'c')
                else:
                    if ncer_flag:
                        base_form = base_form[:len(base_form) - 1] + 'z'
                    else:
                        if ger_gir_flag:
                            base_form = base_form[:len(base_form) - 1] + 'j'
                        else:
                            if car_flag:
                                base_form = base_form[:len(base_form) - 1] + 'qu'
                            if zar_flag:
                                base_form = base_form[:len(base_form) - 1] + 'c'
                        if guir_flag:
                            base_form = base_form[:len(base_form) - 1]
                    if guar_flag:
                        base_form = base_form[:len(base_form) - 1] + 'ü'
            if i in config['tercera_persona'] or i in config['primera_persona']:
                base_form = irregular_cast_group_13_a(verb, base_form, irregular_verb_groups)
                if fnmatch.fnmatch(verb, '*decir'):
                    base_form = base_form.replace('dec', 'dig')
                if fnmatch.fnmatch(verb, '*hacer'):
                    base_form = base_form.replace('hac', 'hag')
            if i in config['segunda_persona']:
                if i in config['singular']:
                    if fnmatch.fnmatch(verb, '*decir'):
                        if mode != 0:
                            base_form = base_form.replace('dec', 'd')
                        suffix_conj[i] = 'í'
                    if fnmatch.fnmatch(verb, '*hacer'):
                        if mode != 0:
                            base_form = base_form.replace('hac', 'ha')
                            suffix_conj[i] = 'z'
                    if mode != 0:
                        base_form = irregular_cast_group_09(verb, base_form, irregular_verb_groups)
            if verb in irregular_verb_groups['irregular_verbs_grupo_07_eir']:
                base_form = base_form[:len(base_form) - 1]
            verb_conj.append(base_form + suffix_conj[i])

        return verb_conj