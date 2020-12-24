# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/objects/images.py
# Compiled at: 2018-10-01 13:52:32
# Size of source mod 2**32: 1129 bytes
from __future__ import absolute_import
from .base import Cloud

class Images(Cloud):
    """Images"""
    path = '/images'

    def __init__(self, api):
        super(Images, self).__init__(api)

    def list(self):
        data = self.api.get(self.get_path())
        return data

    def get(self, id):
        full_path = '{0}/{1}'.format(self.get_path(), id)
        data = self.api.get(full_path)
        return data

    def get_application(self):
        return self.get('?type=application')

    def get_distribution(self):
        return self.get('?type=distribution')

    def get_private(self):
        return self.get('?private=true')

    def rename(self, id, name):
        """
        Change name of snapshot
        """
        payload = {'name': name}
        full_path = '{0}/{1}'.format(self.get_path(), id)
        data = self.api.put(full_path, payload)
        return data

    def delete(self, id):
        """
        Delete image
        """
        full_path = '{0}/{1}'.format(self.get_path(), id)
        data = self.api.delete(full_path)
        return data