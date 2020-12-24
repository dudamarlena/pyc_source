# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/warninghelpers.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import warnings

class PyAlgoTradeDeprecationWarning(DeprecationWarning):
    pass


warnings.simplefilter('default', PyAlgoTradeDeprecationWarning)

def deprecation_warning(msg, stacklevel=0):
    warnings.warn(msg, category=PyAlgoTradeDeprecationWarning, stacklevel=stacklevel + 1)