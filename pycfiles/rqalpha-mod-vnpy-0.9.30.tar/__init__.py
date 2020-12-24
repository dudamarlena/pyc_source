# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/psf/Home/Documents/workspace/rqalpha-mod-vnpy/rqalpha_mod_vnpy/__init__.py
# Compiled at: 2017-05-22 05:49:49
__config__ = {'gateway_type': 'CTP', 
   'vn_trader_path': None, 
   'all_day': True, 
   'query_interval': 2, 
   'default_data_source': True, 
   'temp_path': './vnpy_temp', 
   'CTP': {'userID': None, 
           'password': None, 
           'brokerID': '9999', 
           'tdAddress': 'tcp://180.168.146.187:10030', 
           'mdAddress': 'tcp://180.168.146.187:10031'}}

def load_mod():
    from .mod import VNPYMod
    return VNPYMod()