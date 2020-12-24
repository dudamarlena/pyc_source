# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solo/configurator/compat.py
# Compiled at: 2016-03-29 11:49:28
# Size of source mod 2**32: 615 bytes
""" Parts of this module are taken from ``pyramid.compat`` module
"""
string_types = (
 str,)
integer_types = (int,)
class_types = (type,)
text_type = str
binary_type = bytes
long = int

def is_nonstr_iter(v):
    if isinstance(v, str):
        return False
    return hasattr(v, '__iter__')


def bytes_(s, encoding='latin-1', errors='strict'):
    """ This function is a copy of ``pyramid.compat.bytes_``

    If ``s`` is an instance of ``text_type``, return
    ``s.encode(encoding, errors)``, otherwise return ``s``"""
    if isinstance(s, str):
        return s.encode(encoding, errors)
    return s