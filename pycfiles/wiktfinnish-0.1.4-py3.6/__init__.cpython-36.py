# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wiktfinnish/__init__.py
# Compiled at: 2018-10-31 17:23:05
# Size of source mod 2**32: 796 bytes
from wiktfinnish.formnames import COMP_FORMS, CASE_FORMS, POSSESSIVE_FORMS
from wiktfinnish.formnames import VERB_FORMS, CLITIC_FORMS
from wiktfinnish.formnames import all_forms_list, all_forms_iter
from wiktfinnish.inflect import inflect
from wiktfinnish.inflect import add_clitic
from wiktfinnish.inflect import last_char_to_vowel, last_char_to_aou
from wiktfinnish.inflect import word_to_aae
__all__ = ('inflect', 'add_clitic', 'COMP_FORMS', 'CASE_FORMS', 'POSSESSIVE_FORMS',
           'VERB_FORMS', 'CLITIC_FORMS', 'all_forms_list', 'all_forms_iter', 'last_char_to_vowel',
           'last_char_to_aou', 'word_to_aae')