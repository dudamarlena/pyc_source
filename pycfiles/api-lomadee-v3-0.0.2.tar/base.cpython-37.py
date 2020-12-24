# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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