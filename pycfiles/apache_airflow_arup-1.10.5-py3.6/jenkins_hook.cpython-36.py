# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/jenkins_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1847 bytes
from airflow.hooks.base_hook import BaseHook
import jenkins
from distutils.util import strtobool

class JenkinsHook(BaseHook):
    __doc__ = '\n    Hook to manage connection to jenkins server\n    '

    def __init__(self, conn_id='jenkins_default'):
        connection = self.get_connection(conn_id)
        self.connection = connection
        connectionPrefix = 'http'
        if connection.extra is None or connection.extra == '':
            connection.extra = 'false'
        if strtobool(connection.extra):
            connectionPrefix = 'https'
        url = '%s://%s:%d' % (connectionPrefix, connection.host, connection.port)
        self.log.info('Trying to connect to %s', url)
        self.jenkins_server = jenkins.Jenkins(url, connection.login, connection.password)

    def get_jenkins_server(self):
        return self.jenkins_server