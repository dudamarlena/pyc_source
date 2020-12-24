# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/packages/wordProcessor/spanishConjugator/helpers/participioHelper.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 2339 bytes
import fnmatch

def participio(verb, force_conj, mode, configs):
    irregular_verb_exceptions = configs['irregular_verb_exceptions']
    if not any(fnmatch.fnmatch(verb, suffix) for suffix in ('*ar', '*er', '*ir', '*ár',
                                                            '*ér', '*ír')):
        return ['', '', '']
    else:
        verb_conj = []
        suffix_conj = []
        base_verb = verb[0:len(verb) - 2]
        if verb not in irregular_verb_exceptions.keys() or force_conj:
            if fnmatch.fnmatch(verb, '*ar') or fnmatch.fnmatch(verb, '*ár'):
                suffix_conj = [
                 'ado', 'ada', 'arse']
            if fnmatch.fnmatch(verb, '*er') or fnmatch.fnmatch(verb, '*ér'):
                suffix_conj = [
                 'ido', 'ida', 'erse']
            if fnmatch.fnmatch(verb, '*ir') or fnmatch.fnmatch(verb, '*ír'):
                suffix_conj = [
                 'ido', 'ida', 'irse']
        else:
            return irregular_verb_exceptions[verb]['part']
        for suffix in suffix_conj:
            verb_conj.append(base_verb + suffix)

        if fnmatch.fnmatch(verb, '*olver'):
            verb_conj[0] = verb[0:len(verb) - 5] + 'uelto'
            verb_conj[1] = verb[0:len(verb) - 5] + 'uelta'
        if fnmatch.fnmatch(verb, '*decir'):
            verb_conj[0] = verb[0:len(verb) - 4] + 'icho'
            verb_conj[1] = verb[0:len(verb) - 4] + 'icha'
        if fnmatch.fnmatch(verb, '*hacer'):
            verb_conj[0] = verb[0:len(verb) - 4] + 'echo'
            verb_conj[1] = verb[0:len(verb) - 4] + 'echa'
        if fnmatch.fnmatch(verb, '*pudrir'):
            verb_conj[0] = verb_conj[0].replace('u', 'o', 1)
            verb_conj[1] = verb_conj[1].replace('u', 'o', 1)
        return verb_conj