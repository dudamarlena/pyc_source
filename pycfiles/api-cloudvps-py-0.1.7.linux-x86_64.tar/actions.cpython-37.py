# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/objects/actions.py
# Compiled at: 2018-10-01 13:52:32
# Size of source mod 2**32: 599 bytes
from __future__ import absolute_import
from .base import Cloud

class Actions(Cloud):
    __doc__ = '\n    Module for working with tasks for objects\n    '
    path = '/actions'

    def __init__(self, api):
        super(Actions, self).__init__(api)

    def list(self):
        """
        Get list of active task
        """
        data = self.api.get(self.get_path())
        return data

    def get(self, object_id):
        """
        Get details by task id
        """
        full_path = '{0}/{1}'.format(self.get_path(), object_id)
        data = self.api.get(full_path)
        return data