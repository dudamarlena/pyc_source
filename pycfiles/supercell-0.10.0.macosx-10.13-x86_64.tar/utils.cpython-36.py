# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/utils.py
# Compiled at: 2019-01-08 09:09:15
# Size of source mod 2**32: 1229 bytes
from cgi import escape
from supercell._compat import string_types, text_type
__all__ = [
 'escape_contents']

def escape_contents(o):
    """
    Encodes chars <, > and & as HTML entities.
    """
    _e = escape_contents
    if isinstance(o, string_types):
        return escape(text_type(o))
    else:
        if isinstance(o, dict):
            o = dict([(_e(k), _e(o[k])) for k in o])
        else:
            if isinstance(o, list):
                o = [_e(v) for v in o]
            else:
                if isinstance(o, tuple):
                    o = tuple(_e(v) for v in o)
                else:
                    if isinstance(o, set):
                        o = set([_e(v) for v in o])
        return o