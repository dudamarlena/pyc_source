# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/preteritoPerfSimpleHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 6829 bytes
import fnmatch
from .irregularVerbCastHelper import irregular_cast_group_04_a, irregular_cast_group_06, irregular_cast_group_07, irregular_cast_group_08_b, irregular_cast_group_11, irregular_cast_group_12_b

def preterito_perf_simple_conj(verb, force_conj, mode, configs):
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
        car_flag = False
        zar_flag = False
        guar_flag = False
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                if fnmatch.fnmatch(verb, '*car'):
                    car_flag = True
                elif fnmatch.fnmatch(verb, '*zar'):
                    zar_flag = True
                else:
                    if fnmatch.fnmatch(verb, '*guar'):
                        guar_flag = True
                    if fnmatch.fnmatch(verb, '*gar'):
                        suffix_conj = [
                         'ué', 'aste', 'ó', 'amos', 'asteis', 'aron']
                    else:
                        if fnmatch.fnmatch(verb, '*guar'):
                            suffix_conj = [
                             'üé', 'aste', 'ó', 'amos', 'asteis', 'aron']
                        else:
                            suffix_conj = [
                             'é', 'aste', 'ó', 'amos', 'asteis', 'aron']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = [
                 'í', 'iste', 'ió', 'imos', 'isteis', 'ieron']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = [
                 'í', 'iste', 'ió', 'imos', 'isteis', 'ieron']
        else:
            return irregular_verb_exceptions[verb]['pret_perf']
        for i in range(0, 6):
            if fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'dij')
            else:
                if fnmatch.fnmatch(verb, '*hacer'):
                    base_form = base_verb.replace('hac', 'hic')
                else:
                    base_form = base_verb
                if car_flag:
                    if i in config['primera_persona']:
                        if i in config['singular']:
                            base_form = base_form[:len(base_form) - 1] + 'qu'
                if zar_flag:
                    if i in config['primera_persona']:
                        if i in config['singular']:
                            base_form = base_form[:len(base_form) - 1] + 'c'
                if guar_flag:
                    if i in config['primera_persona']:
                        if i in config['singular']:
                            base_form = base_form[:len(base_form) - 1]
                base_form = irregular_cast_group_04_a(verb, base_form, irregular_verb_groups)
                if i in config['tercera_persona']:
                    if verb in irregular_verb_groups['irregular_verbs_grupo_05_er'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_nir'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_ullir']:
                        suffix_conj[i] = suffix_conj[i][1:]
                    base_form = irregular_cast_group_06(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_07(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_08_b(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_11(verb, base_form, irregular_verb_groups)
                    base_form = irregular_cast_group_12_b(verb, base_form, irregular_verb_groups)
                    if i in config['singular']:
                        if fnmatch.fnmatch(verb, '*hacer'):
                            base_form = base_form[:len(base_form) - 1] + 'z'
                if i in config['tercera_persona']:
                    if verb in irregular_verb_groups['irregular_verbs_grupo_07_eir'] or verb in irregular_verb_groups['irregular_verbs_grupo_07_enir'] or fnmatch.fnmatch(verb, '*uir') and verb not in irregular_verb_groups['irregular_verbs_grupo_06_ir']:
                        suffix_conj[i] = suffix_conj[i][1:]
                if i in config['tercera_persona']:
                    if i in config['plural']:
                        if verb in irregular_verb_groups['irregular_verbs_grupo_04_ducir'] or fnmatch.fnmatch(verb, '*decir'):
                            suffix_conj[i] = suffix_conj[i][1:]
            if i in config['primera_persona']:
                if i in config['singular']:
                    if verb in irregular_verb_groups['irregular_verbs_grupo_04_ducir'] or fnmatch.fnmatch(verb, '*decir') or fnmatch.fnmatch(verb, '*hacer'):
                        verb_conj.append(base_form + 'e')
            elif i in config['tercera_persona']:
                if i in config['singular']:
                    if verb in irregular_verb_groups['irregular_verbs_grupo_04_ducir'] or fnmatch.fnmatch(verb, '*decir') or fnmatch.fnmatch(verb, '*hacer'):
                        verb_conj.append(base_form + 'o')
            else:
                verb_conj.append(base_form + suffix_conj[i])

        return verb_conj