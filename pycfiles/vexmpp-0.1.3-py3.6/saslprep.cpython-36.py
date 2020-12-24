# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vexmpp/suelta/saslprep.py
# Compiled at: 2017-01-31 22:58:59
# Size of source mod 2**32: 2687 bytes
from __future__ import unicode_literals
import sys, stringprep, unicodedata

def saslprep(text, strict=True):
    """
    Return a processed version of the given string, using the SASLPrep
    profile of stringprep.

    :param text: The string to process, in UTF-8.
    :param strict: If ``True``, prevent the use of unassigned code points.
    """
    if sys.version_info < (3, 0):
        if type(text) == str:
            text = text.decode('us-ascii')
    buffer = ''
    for char in text:
        if stringprep.in_table_c12(char):
            buffer += ' '
        else:
            if not stringprep.in_table_b1(char):
                buffer += char

    text = unicodedata.normalize('NFKC', buffer)
    buffer = ''
    first_is_randal = False
    if text:
        first_is_randal = stringprep.in_table_d1(text[0])
        if first_is_randal:
            if not stringprep.in_table_d1(text[(-1)]):
                raise UnicodeError('Section 6.3 [end]')
    for x in range(len(text)):
        if strict:
            if stringprep.in_table_a1(text[x]):
                raise UnicodeError('Unassigned Codepoint')
            else:
                if stringprep.in_table_c12(text[x]):
                    raise UnicodeError('In table C.1.2')
                else:
                    if stringprep.in_table_c21(text[x]):
                        raise UnicodeError('In table C.2.1')
                    else:
                        if stringprep.in_table_c22(text[x]):
                            raise UnicodeError('In table C.2.2')
                        else:
                            if stringprep.in_table_c3(text[x]):
                                raise UnicodeError('In table C.3')
                            else:
                                if stringprep.in_table_c4(text[x]):
                                    raise UnicodeError('In table C.4')
                                if stringprep.in_table_c5(text[x]):
                                    raise UnicodeError('In table C.5')
                            if stringprep.in_table_c6(text[x]):
                                raise UnicodeError('In table C.6')
                        if stringprep.in_table_c7(text[x]):
                            raise UnicodeError('In table C.7')
                    if stringprep.in_table_c8(text[x]):
                        raise UnicodeError('In table C.8')
                if stringprep.in_table_c9(text[x]):
                    raise UnicodeError('In table C.9')
            if x:
                if first_is_randal:
                    if stringprep.in_table_d2(text[x]):
                        raise UnicodeError('Section 6.2')
                if not first_is_randal and x != len(text) - 1 and stringprep.in_table_d1(text[x]):
                    raise UnicodeError('Section 6.3')

    return text