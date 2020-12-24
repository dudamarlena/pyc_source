# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xslcover/config.py
# Compiled at: 2016-11-26 11:29:20
_config_dict = {}

def set_config(**kargs):
    global _config_dict
    _config_dict = kargs


def get_value(param, default=''):
    return _config_dict.get(param, default)