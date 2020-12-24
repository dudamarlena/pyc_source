# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury/common/models/computer.py
# Compiled at: 2018-01-08 12:01:55
# Size of source mod 2**32: 1104 bytes
"""
EVENTUAL CLASS HIERARCHY REPRESENTING INVENTORY/COMPUTER and ACTIVE/COMPUTER
"""
import json

class MercuryID(object):
    pass


class Computer(object):

    def __init__(self):
        self.raw_json_data = None
        self.computer_raw_object = None

    @classmethod
    def from_json(cls, json_data):
        obj = cls()
        obj.raw_json_data = json_data
        obj.computer_raw_object = json.loads(json_data)
        return obj