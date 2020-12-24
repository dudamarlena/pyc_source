# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-ctp/rqalpha_mod_ctp/__init__.py
# Compiled at: 2017-05-26 23:16:26
__config__ = {'login': {'user_id': None, 
             'password': None, 
             'broker_id': '9999'}, 
   'event': {'enabled': True, 
             'all_day': False, 
             'address': 'tcp://180.168.212.228:41213'}, 
   'trade': {'enabled': True, 
             'address': 'tcp://180.168.146.187:10000'}}

def load_mod():
    from .mod import CtpMod
    return CtpMod()