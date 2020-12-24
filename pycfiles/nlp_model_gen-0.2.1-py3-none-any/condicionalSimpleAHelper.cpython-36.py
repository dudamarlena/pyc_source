# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/condicionalSimpleAHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 2418 bytes
import fnmatch
from .irregularVerbCastHelper import irregular_cast_group_13_b

def condicional_simple_A_conj(verb, force_conj, mode, configs):
    irregular_verb_exceptions = configs['irregular_verb_exceptions']
    irregular_verb_groups = configs['irregular_verb_groups']
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ('*ar', '*er', '*ir', '*ár',
                                                            '*ér', '*ír')):
        return ['', '', '', '', '', '']
    else:
        verb_conj = []
        suffix_conj = []
        if fnmatch.fnmatch(verb, '*hacer'):
            verb = verb.replace('hacer', 'hacar')
        base_verb = verb[0:len(verb) - 2]
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = [
                 'aría', 'arías', 'aría', 'aríamos', 'aríais', 'arían']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = [
                 'ería', 'erías', 'ería', 'eríamos', 'eríais', 'erían']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = [
                 'iría', 'irías', 'iría', 'iríamos', 'iríais', 'irían']
        else:
            return irregular_verb_exceptions[verb]['condA']
        for suffix in suffix_conj:
            if fnmatch.fnmatch(verb, '*decir'):
                base_form = base_verb.replace('dec', 'd')
            else:
                if fnmatch.fnmatch(verb, '*hacar'):
                    base_form = base_verb.replace('hac', 'h')
                else:
                    base_form = base_verb
            base_form = irregular_cast_group_13_b(verb, base_form, irregular_verb_groups)
            if verb in irregular_verb_groups['irregular_verbs_grupo_13_alir'] or verb in irregular_verb_groups['irregular_verbs_grupo_13_aler']:
                suffix = suffix[1:]
            verb_conj.append(base_form + suffix)

        return verb_conj