# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Brett\Git\verbecc\verbecc\exceptions.py
# Compiled at: 2019-07-07 11:52:43
# Size of source mod 2**32: 453 bytes


class ConjugatorError(Exception):
    pass


class ConjugationsParserError(Exception):
    pass


class ConjugationTemplateError(Exception):
    pass


class InvalidLangError(Exception):
    pass


class InvalidMoodError(Exception):
    pass


class InvalidTenseError(Exception):
    pass


class TemplateNotFoundError(Exception):
    pass


class VerbNotFoundError(Exception):
    pass


class VerbsParserError(Exception):
    pass