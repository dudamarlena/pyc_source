# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/jenkins_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1847 bytes
from airflow.hooks.base_hook import BaseHook
import jenkins
from distutils.util import strtobool

class JenkinsHook(BaseHook):
    """JenkinsHook"""

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