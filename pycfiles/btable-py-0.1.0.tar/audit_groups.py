# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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