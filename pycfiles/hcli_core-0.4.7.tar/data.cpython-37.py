# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeff/Documents/workspace/hcli/hcli_core/hcli_core/sample/nw/cli/data.py
# Compiled at: 2019-07-13 20:52:00
# Size of source mod 2**32: 1168 bytes
import json, os
try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace

class DAO:
    path = os.path.dirname(__file__)

    def __init__(self, model=None):
        if model is not None:
            for key, value in vars(model).items():
                setattr(self, key, value)

    def serialize(self):
        return json.dumps(self, default=(lambda o: o.__dict__), sort_keys=True,
          indent=4)

    def exists(self):
        if not os.path.exists(self.path + '/networks.json'):
            return False
        return True

    def save(self):
        with open(self.path + '/networks.json', 'w') as (f):
            f.write(self.serialize())
            f.close()

    def load(self, obj):
        with open(self.path + '/networks.json', 'r') as (f):
            j = f.read()
            f.close()
            obj.__dict__ = json.loads(j)