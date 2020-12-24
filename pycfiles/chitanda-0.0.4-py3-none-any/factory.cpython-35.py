# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/repos/factory.py
# Compiled at: 2018-10-02 19:35:34
# Size of source mod 2**32: 1336 bytes
from builtins import object
from chisubmit.repos import ConnectionString
from chisubmit.common import ChisubmitException
from chisubmit.repos.github import GitHubConnection
from chisubmit.repos.gitlab import GitLabConnection
from chisubmit.repos.testing import TestingConnection

class RemoteRepositoryConnectionFactory(object):
    server_types = {}

    @staticmethod
    def register_server_type(name, conn_cls):
        RemoteRepositoryConnectionFactory.server_types[name] = conn_cls

    @staticmethod
    def create_connection(connection_string, staging, ssl_verify=True):
        cs = ConnectionString(connection_string)
        if cs.server_type not in RemoteRepositoryConnectionFactory.server_types:
            raise ChisubmitException('Unsupported server type in connection string: %s (expected one of: %s)' % (
             cs.server_type, ', '.join(list(RemoteRepositoryConnectionFactory.server_types.keys()))))
        conn_cls = RemoteRepositoryConnectionFactory.server_types[cs.server_type]
        return conn_cls(cs, staging, ssl_verify)


RemoteRepositoryConnectionFactory.register_server_type('GitHub', GitHubConnection)
RemoteRepositoryConnectionFactory.register_server_type('GitLab', GitLabConnection)
RemoteRepositoryConnectionFactory.register_server_type('Testing', TestingConnection)