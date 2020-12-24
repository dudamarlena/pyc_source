# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/indentation.py
# Compiled at: 2020-03-06 05:24:58
# Size of source mod 2**32: 323 bytes
"""Indentation for Buildout Versions Checker"""

def perfect_indentation(keys, rounding=4):
    """
    Find perfect indentation by iterating over keys.
    """
    max_key_length = max((len(k) for k in keys))
    indentation = max_key_length + (rounding - max_key_length % rounding)
    return indentation