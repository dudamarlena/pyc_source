# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/gerundioHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 2783 bytes
import fnmatch
from .irregularVerbCastHelper import irregular_cast_group_06, irregular_cast_group_07, irregular_cast_group_11, irregular_cast_group_12_b

def gerundio(verb, force_conj, mode, configs):
    irregular_verb_exceptions = configs['irregular_verb_exceptions']
    irregular_verb_groups = configs['irregular_verb_groups']
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ('*ar', '*er', '*ir', '*ár',
                                                            '*ér', '*ír')):
        return ['']
    else:
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb) - 2]
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = [
                 'ando']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = [
                 'iendo']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = [
                 'iendo']
        else:
            return irregular_verb_exceptions[verb]['ger']
        for suffix in suffix_conj:
            base_form = base_verb
            base_form = irregular_cast_group_06(verb, base_form, irregular_verb_groups)
            base_form = irregular_cast_group_07(verb, base_form, irregular_verb_groups)
            base_form = irregular_cast_group_11(verb, base_form, irregular_verb_groups)
            base_form = irregular_cast_group_12_b(verb, base_form, irregular_verb_groups)
            if verb in irregular_verb_groups['irregular_verbs_grupo_11_uir'] or verb in irregular_verb_groups['irregular_verbs_grupo_07_eir'] or verb in irregular_verb_groups['irregular_verbs_grupo_07_enir'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_er'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_nir'] or verb in irregular_verb_groups['irregular_verbs_grupo_05_ullir']:
                suffix = suffix[1:]
            verb_conj.append(base_form + suffix)

        return verb_conj