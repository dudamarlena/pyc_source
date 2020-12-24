# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/audit_uac.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner, MinerList

@Miner.register
class UAC_Audit(MinerList):
    _name_ = 'Audit_UAC'
    _desc_ = 'Run all analyses on User Account Control'
    _report_ = [
     ('CheckUAC', 'accountDisable'),
     ('CheckUAC', 'passwdNotrequired'),
     ('CheckUAC', 'passwdCantChange'),
     ('CheckUAC', 'dontExpirePassword')]