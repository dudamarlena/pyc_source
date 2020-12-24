# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/audit_groups.py
# Compiled at: 2014-07-11 17:28:37
from bta.miner import Miner, MinerList

@Miner.register
class Groups_Audit(MinerList):
    _name_ = 'Audit_Groups'
    _desc_ = 'Run all analyses on groups'
    _report_ = [
     ('ListGroup', '--match', 'Domain Admins'),
     ('ListGroup', '--match', 'Enterprise Admins')]