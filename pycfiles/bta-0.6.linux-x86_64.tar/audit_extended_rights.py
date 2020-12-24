# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/bta/miners/audit_extended_rights.py
# Compiled at: 2014-07-11 17:28:37
from bta.miner import Miner, MinerList

@Miner.register
class ExtendedRights_Audit(MinerList):
    _name_ = 'Audit_ExtRights'
    _desc_ = 'Run all analyses on extended rights'
    _report_ = [
     ('ListACE', '--type', '00299570-246d-11d0-a768-00aa006e0529'),
     ('ListACE', '--type', 'ab721a54-1e2f-11d0-9819-00aa0040529b'),
     ('ListACE', '--type', 'bf9679c0-0de6-11d0-a285-00aa003049e2')]