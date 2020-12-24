# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/docker_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 3179 bytes
from docker import APIClient
from docker.errors import APIError
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin

class DockerHook(BaseHook, LoggingMixin):
    __doc__ = '\n    Interact with a private Docker registry.\n\n    :param docker_conn_id: ID of the Airflow connection where\n        credentials and extra configuration are stored\n    :type docker_conn_id: str\n    '

    def __init__(self, docker_conn_id='docker_default', base_url=None, version=None, tls=None):
        if not base_url:
            raise AirflowException('No Docker base URL provided')
        else:
            if not version:
                raise AirflowException('No Docker API version provided')
            else:
                conn = self.get_connection(docker_conn_id)
                if not conn.host:
                    raise AirflowException('No Docker registry URL provided')
                raise conn.login or AirflowException('No username provided')
            extra_options = conn.extra_dejson
            self._DockerHook__base_url = base_url
            self._DockerHook__version = version
            self._DockerHook__tls = tls
            if conn.port:
                self._DockerHook__registry = '{}:{}'.format(conn.host, conn.port)
            else:
                self._DockerHook__registry = conn.host
        self._DockerHook__username = conn.login
        self._DockerHook__password = conn.password
        self._DockerHook__email = extra_options.get('email')
        self._DockerHook__reauth = False if extra_options.get('reauth') == 'no' else True

    def get_conn(self):
        client = APIClient(base_url=(self._DockerHook__base_url),
          version=(self._DockerHook__version),
          tls=(self._DockerHook__tls))
        self._DockerHook__login(client)
        return client

    def __login(self, client):
        self.log.debug('Logging into Docker registry')
        try:
            client.login(username=(self._DockerHook__username),
              password=(self._DockerHook__password),
              registry=(self._DockerHook__registry),
              email=(self._DockerHook__email),
              reauth=(self._DockerHook__reauth))
            self.log.debug('Login successful')
        except APIError as docker_error:
            self.log.error('Docker registry login failed: %s', str(docker_error))
            raise AirflowException('Docker registry login failed: %s', str(docker_error))