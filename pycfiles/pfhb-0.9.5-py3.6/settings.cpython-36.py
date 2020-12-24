# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/src/settings.py
# Compiled at: 2019-02-21 13:26:14
# Size of source mod 2**32: 1488 bytes
PF_CONFIG_SOURCE = '/etc/pf.conf'
PF_CONFIG_TARGET = 'pf.pfhb.conf'
PF_LOG_RULES = True
PF_INBOUND_INTERFACE = '$int_if'
PF_IPS_TO_BLOCK = [
 '192.168.0.0/24']
PF_IPS_TO_ALLOW = [
 '192.168.0.10']
PF_RELOAD_COMMAND = 'pfctl -f'
REDIS = {'host':'127.0.0.1', 
 'port':6379, 
 'password':'', 
 'db':0}
INSANE_MODE = False