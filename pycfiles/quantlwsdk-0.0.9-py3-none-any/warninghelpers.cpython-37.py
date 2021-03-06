# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\warninghelpers.py
# Compiled at: 2019-06-05 03:26:24
# Size of source mod 2**32: 1091 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import warnings

class PyAlgoTradeDeprecationWarning(DeprecationWarning):
    pass


warnings.simplefilter('default', PyAlgoTradeDeprecationWarning)

def deprecation_warning(msg, stacklevel=0):
    warnings.warn(msg, category=PyAlgoTradeDeprecationWarning, stacklevel=(stacklevel + 1))