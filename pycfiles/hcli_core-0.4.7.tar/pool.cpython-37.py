# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeff/Documents/workspace/hcli/hcli_core/hcli_core/sample/nw/cli/pool.py
# Compiled at: 2019-07-28 17:58:55
# Size of source mod 2**32: 418 bytes
import json, data

class Pool:
    name = None
    allocated = None
    free = None

    def __init__(self, groupname, networks=None):
        self.name = groupname
        self.allocated = []
        if networks != None:
            self.free = [
             '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16']
        else:
            self.free = []

    def serialize(self):
        return data.DAO(self).serialize()