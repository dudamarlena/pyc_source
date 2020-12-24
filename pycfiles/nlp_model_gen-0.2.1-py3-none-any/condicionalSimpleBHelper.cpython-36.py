# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/condicionalSimpleBHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 4143 bytes
import fnmatch
from .irregularVerbCastHelper import irregular_cast_group_04_a, irregular_cast_group_06, irregular_cast_group_07, irregular_cast_group_08_b, irregular_cast_group_12_b

def condicional_simple_B_conj(verb, force_conj, mode, configs):
    irregular_verb_exceptions = configs['irregular_verb_exceptions']
    irregular_verb_groups = configs['irregular_verb_groups']
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ('*ar', '*er', '*ir', '*ár',
                                                            '*ér', '*ír')):
        return ['', '', '', '', '', '']
    else:
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb) - 2]
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = [
                 'ase', 'ases', 'ase', 'ásemos', 'aseis', 'asen']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = [
                 'iese', 'ieses', 'iese', 'iésemos', 'ieseis', 'iesen']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = [
                 'iese', 'ieses', 'iese', 'iésemos', 'ieseis', 'iesen']
        else:
            return irregular_verb_exceptions[verb]['condB']
        for i in range(0, 6):
            if fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'dij')
            else:
                if fnmatch.fnmatch(verb, '*hacer'):
                    base_form = base_verb.replace('hac', 'hic')
                else:
                    base_form = base_verb
                base_form = irregular_cast_group_04_a(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_06(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_07(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_08_b(verb, base_form, irregular_verb_groups)
                base_form = irregular_cast_group_12_b(verb, base_form, irregular_verb_groups)
                if fnmatch.fnmatch(verb, '*uir'):
                    if verb not in irregular_verb_groups['irregular_verbs_grupo_06_ir']:
                        base_form += 'y'
                if verb in irregular_verb_groups['irregular_verbs_grupo_04_ducir'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_er'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_nir'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_ullir'] or verb in irregular_verb_groups['irregular_verbs_grupo_07_eir'] or verb in irregular_verb_groups['irregular_verbs_grupo_07_enir'] or fnmatch.fnmatch(verb, '*uir') and verb not in irregular_verb_groups['irregular_verbs_grupo_06_ir'] or fnmatch.fnmatch(verb, '*decir'):
                    if fnmatch.fnmatch(suffix_conj[i], 'i*'):
                        suffix_conj[i] = suffix_conj[i][1:]
            verb_conj.append(base_form + suffix_conj[i])

        return verb_conj