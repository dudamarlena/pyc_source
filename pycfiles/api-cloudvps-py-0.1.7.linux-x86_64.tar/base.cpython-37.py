# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/objects/base.py
# Compiled at: 2018-01-31 04:38:44
# Size of source mod 2**32: 360 bytes
from builtins import object

class Cloud(object):
    api = None
    path = None

    def __init__(self, api):
        self.api = api

    def list(self):
        pass

    def get(self):
        pass

    def create(self):
        pass

    def rename(self):
        pass

    def delete(self):
        pass

    def get_path(self):
        return self.path