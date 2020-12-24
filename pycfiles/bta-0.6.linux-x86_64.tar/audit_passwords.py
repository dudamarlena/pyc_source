# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/audit_passwords.py
# Compiled at: 2015-10-20 16:27:01
from bta.miner import Miner, MinerList

@Miner.register
class Audit_Passwords(MinerList):
    _name_ = 'Audit_Passwords'
    _desc_ = 'Run all analyses on passwords'
    _report_ = [
     ('passwords', '--never-logged'),
     ('passwords', '--last-logon', '1215'),
     ('passwords', '--last-logon', '485'),
     ('passwords', '--last-logon', '302'),
     ('passwords', '--bad-password-count')]