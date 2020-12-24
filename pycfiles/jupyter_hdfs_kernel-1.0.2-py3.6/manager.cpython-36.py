# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/connections/manager.py
# Compiled at: 2020-01-16 03:10:17
# Size of source mod 2**32: 1440 bytes
from hdfs_kernel.utils.loggers import HdfsLog
from hdfs_kernel.exceptions import SessionManagementException
from hdfs_kernel.connections.hdfs_client import HdfsKerberosClient

class HdfsSessionManager(object):

    def __init__(self, client_class=None):
        self.client_class = client_class or HdfsKerberosClient
        self.logger = HdfsLog(__name__)
        self._sessions = dict()

    def get(self, nameservice):
        return self._sessions.get(nameservice)

    def add_session(self, nameservice, session):
        self._sessions[nameservice] = session
        self.logger.info('Create Hdfs Session: %s ' % nameservice)

    def delete_by_nameservice(self, nameservice):
        session = self._sessions.get(nameservice)
        if not session:
            raise SessionManagementException(f"Could not find '{nameservice}' session")
        self._sessions[nameservice].close()
        del self._sessions[nameservice]
        self.logger.info('Hdfs Session: %s deleted' % nameservice)

    def get_or_init(self, nameservice):
        session = self.get(nameservice)
        if not session:
            session = self.client_class(nameservice)
            self.add_session(nameservice, session)
        return session

    def __call__(self, nameservice):
        return self.get_or_init(nameservice)