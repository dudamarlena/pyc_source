# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/objects/history.py
# Compiled at: 2018-10-01 13:52:32
# Size of source mod 2**32: 590 bytes
from __future__ import absolute_import
from .base import Cloud

class History(Cloud):
    __doc__ = '\n    Module for obtaining operation history\n    '
    path = '/history'

    def __init__(self, api):
        super(History, self).__init__(api)

    def list(self):
        """
        Get all history
        """
        data = self.api.get(self.get_path())
        return data

    def get(self, object_id):
        """
        Get history by object_id
        """
        full_path = '{0}/{1}'.format(self.get_path(), object_id)
        data = self.api.get(full_path)
        return data