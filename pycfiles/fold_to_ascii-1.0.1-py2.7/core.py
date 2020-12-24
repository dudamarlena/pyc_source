# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/fold_to_ascii/core.py
# Compiled at: 2017-11-01 20:00:13
from __future__ import print_function
from collections import defaultdict
from . import mapping

def none_factory():
    return


default_translate_table = defaultdict(none_factory, mapping.translate_table)

def fold(unicode_string, replacement=''):
    """Fold unicode_string to ASCII.

Unmapped characters should be replaced with empty string by default, or other
replacement if provided.

All astral plane characters are always removed, even if a replacement is
provided.
    """
    if unicode_string is None:
        return ''
    else:
        if type(unicode_string) != unicode:
            raise TypeError('cannot fold bytestring')
        if type(replacement) != unicode:
            raise TypeError('cannot replace using bytestring')
        try:
            unicode_string.decode('ascii')
            return unicode_string
        except (UnicodeDecodeError, UnicodeEncodeError) as ex:
            pass

        if replacement:

            def replacement_factory():
                return replacement

            translate_table = defaultdict(replacement_factory, mapping.translate_table)
        else:
            translate_table = default_translate_table
        return unicode_string.translate(translate_table)