# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grudin/dev/my/api-cloudvps-py/.venv/lib/python3.7/site-packages/cloudvps/objects/ssh_keys.py
# Compiled at: 2018-10-01 13:52:32
# Size of source mod 2**32: 1083 bytes
from __future__ import absolute_import
from .base import Cloud

class SshKeys(Cloud):
    __doc__ = '\n    Module for ssh keys storage\n    '
    path = '/account/keys'

    def __init__(self, api):
        super(SshKeys, self).__init__(api)

    def list(self):
        data = self.api.get(self.get_path())
        return data

    def create(self, name, public_key):
        """
        Add new ssh-key
        require fields: name, public_key
        """
        payload = {}
        payload['name'] = name
        payload['public_key'] = public_key
        data = self.api.post(self.get_path(), payload)
        return data

    def rename(self, id, name):
        """
        Change name of ssh key
        """
        payload = {'name': name}
        full_path = '{0}/{1}'.format(self.get_path(), id)
        data = self.api.put(full_path, payload)
        return data

    def delete(self, id):
        """
        Delete key from key-storage
        """
        full_path = '{0}/{1}'.format(self.get_path(), id)
        data = self.api.delete(full_path)
        return data