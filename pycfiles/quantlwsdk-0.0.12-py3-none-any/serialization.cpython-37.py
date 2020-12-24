# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SH\AppData\Local\Temp\pip-install-1sehz1ij\PyAlgoTrade\pyalgotrade\optimizer\serialization.py
# Compiled at: 2018-10-21 21:07:45
# Size of source mod 2**32: 975 bytes
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import pickle, six
from six.moves import xmlrpc_client

def dumps(obj):
    return pickle.dumps(obj)


def loads(serialized):
    if six.PY3:
        if isinstance(serialized, xmlrpc_client.Binary):
            serialized = serialized.data
    return pickle.loads(serialized)