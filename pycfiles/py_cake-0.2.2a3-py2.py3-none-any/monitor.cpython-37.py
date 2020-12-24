# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\graph\hummer\hummber_gang_chat_new\servicemesh\monitor.py
# Compiled at: 2019-05-31 07:38:24
# Size of source mod 2**32: 313 bytes


def info():
    return {'name':'Demo', 
     'author':'chuter', 
     'version':'0.0.1'}


def health():
    return {'cpu':8, 
     'mem':6000, 
     'net':0.5}


def metrics():
    return 'Metrics'