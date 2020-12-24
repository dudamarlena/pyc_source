# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/deployer/ansible/role.py
# Compiled at: 2017-04-23 10:30:41
import os.path

class AnsibleRole(object):

    def __init__(self, uri, hosts='all', become=True, variables=None, group='all'):
        assert uri is not None
        self.uri = uri
        self.path = self._materialize_uri(self.uri)
        self.name = os.path.basename(self.path)
        self.hosts = hosts
        self.directory = os.path.dirname(self.path)
        self.become = become
        self.variables = variables or {}
        self.group = group
        return

    def _materialize_uri(self, uri):
        if os.path.exists(uri):
            return uri
        if uri.startswith('file://'):
            return uri.lstrip('file://')
        raise NotImplementedError(uri)