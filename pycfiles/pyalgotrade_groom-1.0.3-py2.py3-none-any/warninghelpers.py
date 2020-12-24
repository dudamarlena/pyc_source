# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/warninghelpers.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
import warnings

class PyAlgoTradeDeprecationWarning(DeprecationWarning):
    pass


warnings.simplefilter('default', PyAlgoTradeDeprecationWarning)

def deprecation_warning(msg, stacklevel=0):
    warnings.warn(msg, category=PyAlgoTradeDeprecationWarning, stacklevel=stacklevel + 1)