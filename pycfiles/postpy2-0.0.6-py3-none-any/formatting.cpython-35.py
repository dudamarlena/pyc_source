# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/postpy/formatting.py
# Compiled at: 2017-10-20 11:11:37
# Size of source mod 2**32: 414 bytes
__doc__ = 'Formatting helpers.'
from types import MappingProxyType
PYFORMAT = 'pyformat'
NAMED_STYLE = 'named_style'

def pyformat_parameters(parameters):
    return ', '.join(['%s'] * len(parameters))


def named_style_parameters(parameters):
    return ', '.join('%({})s'.format(p) for p in parameters)


PARAM_STYLES = MappingProxyType({PYFORMAT: pyformat_parameters, 
 NAMED_STYLE: named_style_parameters})