# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/hdfs_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3967 bytes
from airflow import configuration
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
try:
    from snakebite.client import Client, HAClient, Namenode, AutoConfigClient
    snakebite_loaded = True
except ImportError:
    snakebite_loaded = False

class HDFSHookException(AirflowException):
    pass


class HDFSHook(BaseHook):
    __doc__ = "\n    Interact with HDFS. This class is a wrapper around the snakebite library.\n\n    :param hdfs_conn_id: Connection id to fetch connection info\n    :type hdfs_conn_id: str\n    :param proxy_user: effective user for HDFS operations\n    :type proxy_user: str\n    :param autoconfig: use snakebite's automatically configured client\n    :type autoconfig: bool\n    "

    def __init__(self, hdfs_conn_id='hdfs_default', proxy_user=None, autoconfig=False):
        if not snakebite_loaded:
            raise ImportError('This HDFSHook implementation requires snakebite, but snakebite is not compatible with Python 3 (as of August 2015). Please use Python 2 if you require this hook  -- or help by submitting a PR!')
        self.hdfs_conn_id = hdfs_conn_id
        self.proxy_user = proxy_user
        self.autoconfig = autoconfig

    def get_conn(self):
        """
        Returns a snakebite HDFSClient object.
        """
        effective_user = self.proxy_user
        autoconfig = self.autoconfig
        use_sasl = configuration.conf.get('core', 'security') == 'kerberos'
        try:
            connections = self.get_connections(self.hdfs_conn_id)
            if not effective_user:
                effective_user = connections[0].login
            if not autoconfig:
                autoconfig = connections[0].extra_dejson.get('autoconfig', False)
            hdfs_namenode_principal = connections[0].extra_dejson.get('hdfs_namenode_principal')
        except AirflowException:
            if not autoconfig:
                raise

        if autoconfig:
            client = AutoConfigClient(effective_user=effective_user, use_sasl=use_sasl)
        else:
            if len(connections) == 1:
                client = Client((connections[0].host), (connections[0].port), effective_user=effective_user,
                  use_sasl=use_sasl,
                  hdfs_namenode_principal=hdfs_namenode_principal)
            else:
                if len(connections) > 1:
                    nn = [Namenode(conn.host, conn.port) for conn in connections]
                    client = HAClient(nn, effective_user=effective_user, use_sasl=use_sasl,
                      hdfs_namenode_principal=hdfs_namenode_principal)
                else:
                    raise HDFSHookException("conn_id doesn't exist in the repository and autoconfig is not specified")
        return client