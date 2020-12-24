# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/formatting.py
# Compiled at: 2017-10-20 11:11:37
# Size of source mod 2**32: 414 bytes
"""Formatting helpers."""
from types import MappingProxyType
PYFORMAT = 'pyformat'
NAMED_STYLE = 'named_style'

def pyformat_parameters(parameters):
    return ', '.join(['%s'] * len(parameters))


def named_style_parameters(parameters):
    return ', '.join('%({})s'.format(p) for p in parameters)


PARAM_STYLES = MappingProxyType({PYFORMAT: pyformat_parameters, 
 NAMED_STYLE: named_style_parameters})