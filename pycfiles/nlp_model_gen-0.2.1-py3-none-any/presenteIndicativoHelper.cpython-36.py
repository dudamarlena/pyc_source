# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/presenteIndicativoHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 7144 bytes
import fnmatch
from .irregularVerbCastHelper import irregular_cast_group_01, irregular_cast_group_02, irregular_cast_group_03, irregular_cast_group_04_b, irregular_cast_group_06, irregular_cast_group_07, irregular_cast_group_08_a, irregular_cast_group_09, irregular_cast_group_10, irregular_cast_group_11, irregular_cast_group_12_a, irregular_cast_group_13_a

def presente_conj(verb, force_conj, mode, configs):
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
        guir_flag = False
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                if mode == 0:
                    suffix_conj = [
                     'o', 'ás', 'a', 'amos', 'áis', 'an']
                else:
                    suffix_conj = [
                     'o', 'as', 'a', 'amos', 'áis', 'an']
                if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                    if fnmatch.fnmatch(verb, '*ncer'):
                        ncer_flag = True
                    if fnmatch.fnmatch(verb, '*ger'):
                        ger_gir_flag = True
                    if mode == 0:
                        suffix_conj = [
                         'o', 'és', 'e', 'emos', 'éis', 'en']
                    else:
                        suffix_conj = [
                         'o', 'es', 'e', 'emos', 'éis', 'en']
                    if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                        if fnmatch.fnmatch(verb, '*gir'):
                            ger_gir_flag = True
                        if fnmatch.fnmatch(verb, '*guir'):
                            guir_flag = True
                        if mode == 0:
                            suffix_conj = [
                             'o', 'ís', 'e', 'imos', 'ís', 'en']
                        else:
                            suffix_conj = [
                             'o', 'es', 'e', 'imos', 'ís', 'en']
        else:
            return irregular_verb_exceptions[verb]['pres']
        for i in range(0, 6):
            base_form = base_verb
            if i in config['singular'] and not mode == 0 or mode == 0 and i in config['singular'] and i not in config['segunda_persona'] or i in config['plural'] and i in config['tercera_persona']:
                base_form = irregular_cast_group_01(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_02(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_06(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_07(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_08_a(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_09(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_10(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_11(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_12_a(verb, base_form, irregular_verb_groups)
                if fnmatch.fnmatch(verb, '*decir'):
                    if i not in config['primera_persona']:
                        base_form = base_form.replace('dec', 'dic')
            if i in config['singular']:
                if i in config['primera_persona']:
                    if ncer_flag:
                        base_form = base_form[:len(base_form) - 1] + 'z'
                    else:
                        if ger_gir_flag:
                            base_form = base_form[:len(base_form) - 1] + 'j'
                        else:
                            if guir_flag:
                                base_form = base_form[:len(base_form) - 2] + 'g'
                            if fnmatch.fnmatch(verb, '*decir'):
                                base_form = base_form.replace('dec', 'dig')
                        if fnmatch.fnmatch(verb, '*hacer'):
                            base_form = base_form[:len(base_form) - 1] + 'g'
                    base_form = irregular_cast_group_03(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_04_b(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_13_a(verb, base_form, irregular_verb_groups)
                verb_conj.append(base_form + suffix_conj[i])
                if verb == 'delinquir' and i in config['primera_persona'] and i in config['singular']:
                    verb_conj[-1] = 'delinco'

        return verb_conj