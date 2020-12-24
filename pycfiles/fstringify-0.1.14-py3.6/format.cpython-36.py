# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fstringify/format.py
# Compiled at: 2018-12-17 02:52:30
# Size of source mod 2**32: 529 bytes
import re, black

class Leaf:
    __doc__ = 'Bare minimum implemention of black `Leaf`'

    def __init__(self, value):
        self.value = value


def force_double_quote_fstring(code):
    """Use black's `normalize_string`_quotes`"""
    result = re.findall("\\b(f'[^']+')", code)
    if not result:
        return code
    else:
        org = result[0]
        if '"' in org or '\\' in org:
            return code
        leaf = Leaf(org)
        black.normalize_string_quotes(leaf)
        return code.replace(org, leaf.value)