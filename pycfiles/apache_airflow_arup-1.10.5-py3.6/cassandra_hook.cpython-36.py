# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/cassandra_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 7657 bytes
from cassandra.cluster import Cluster
from cassandra.policies import RoundRobinPolicy, DCAwareRoundRobinPolicy, TokenAwarePolicy, WhiteListRoundRobinPolicy
from cassandra.auth import PlainTextAuthProvider
from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin

class CassandraHook(BaseHook, LoggingMixin):
    __doc__ = "\n    Hook used to interact with Cassandra\n\n    Contact points can be specified as a comma-separated string in the 'hosts'\n    field of the connection.\n\n    Port can be specified in the port field of the connection.\n\n    If SSL is enabled in Cassandra, pass in a dict in the extra field as kwargs for\n    ``ssl.wrap_socket()``. For example::\n\n        {\n            'ssl_options' : {\n                'ca_certs' : PATH_TO_CA_CERTS\n            }\n        }\n\n    Default load balancing policy is RoundRobinPolicy. To specify a different\n    LB policy::\n\n        - DCAwareRoundRobinPolicy\n            {\n                'load_balancing_policy': 'DCAwareRoundRobinPolicy',\n                'load_balancing_policy_args': {\n                    'local_dc': LOCAL_DC_NAME,                      // optional\n                    'used_hosts_per_remote_dc': SOME_INT_VALUE,     // optional\n                }\n             }\n        - WhiteListRoundRobinPolicy\n            {\n                'load_balancing_policy': 'WhiteListRoundRobinPolicy',\n                'load_balancing_policy_args': {\n                    'hosts': ['HOST1', 'HOST2', 'HOST3']\n                }\n            }\n        - TokenAwarePolicy\n            {\n                'load_balancing_policy': 'TokenAwarePolicy',\n                'load_balancing_policy_args': {\n                    'child_load_balancing_policy': CHILD_POLICY_NAME, // optional\n                    'child_load_balancing_policy_args': { ... }       // optional\n                }\n            }\n\n    For details of the Cluster config, see cassandra.cluster.\n    "

    def __init__(self, cassandra_conn_id='cassandra_default'):
        conn = self.get_connection(cassandra_conn_id)
        conn_config = {}
        if conn.host:
            conn_config['contact_points'] = conn.host.split(',')
        if conn.port:
            conn_config['port'] = int(conn.port)
        if conn.login:
            conn_config['auth_provider'] = PlainTextAuthProvider(username=(conn.login),
              password=(conn.password))
        policy_name = conn.extra_dejson.get('load_balancing_policy', None)
        policy_args = conn.extra_dejson.get('load_balancing_policy_args', {})
        lb_policy = self.get_lb_policy(policy_name, policy_args)
        if lb_policy:
            conn_config['load_balancing_policy'] = lb_policy
        cql_version = conn.extra_dejson.get('cql_version', None)
        if cql_version:
            conn_config['cql_version'] = cql_version
        ssl_options = conn.extra_dejson.get('ssl_options', None)
        if ssl_options:
            conn_config['ssl_options'] = ssl_options
        self.cluster = Cluster(**conn_config)
        self.keyspace = conn.schema
        self.session = None

    def get_conn(self):
        """
        Returns a cassandra Session object
        """
        if self.session:
            if not self.session.is_shutdown:
                return self.session
        self.session = self.cluster.connect(self.keyspace)
        return self.session

    def get_cluster(self):
        return self.cluster

    def shutdown_cluster(self):
        """
        Closes all sessions and connections associated with this Cluster.
        """
        if not self.cluster.is_shutdown:
            self.cluster.shutdown()

    @staticmethod
    def get_lb_policy(policy_name, policy_args):
        policies = {'RoundRobinPolicy':RoundRobinPolicy, 
         'DCAwareRoundRobinPolicy':DCAwareRoundRobinPolicy, 
         'WhiteListRoundRobinPolicy':WhiteListRoundRobinPolicy, 
         'TokenAwarePolicy':TokenAwarePolicy}
        if not policies.get(policy_name) or policy_name == 'RoundRobinPolicy':
            return RoundRobinPolicy()
        if policy_name == 'DCAwareRoundRobinPolicy':
            local_dc = policy_args.get('local_dc', '')
            used_hosts_per_remote_dc = int(policy_args.get('used_hosts_per_remote_dc', 0))
            return DCAwareRoundRobinPolicy(local_dc, used_hosts_per_remote_dc)
        if policy_name == 'WhiteListRoundRobinPolicy':
            hosts = policy_args.get('hosts')
            if not hosts:
                raise Exception('Hosts must be specified for WhiteListRoundRobinPolicy')
            return WhiteListRoundRobinPolicy(hosts)
        if policy_name == 'TokenAwarePolicy':
            allowed_child_policies = ('RoundRobinPolicy', 'DCAwareRoundRobinPolicy',
                                      'WhiteListRoundRobinPolicy')
            child_policy_name = policy_args.get('child_load_balancing_policy', 'RoundRobinPolicy')
            child_policy_args = policy_args.get('child_load_balancing_policy_args', {})
            if child_policy_name not in allowed_child_policies:
                return TokenAwarePolicy(RoundRobinPolicy())
            else:
                child_policy = CassandraHook.get_lb_policy(child_policy_name, child_policy_args)
                return TokenAwarePolicy(child_policy)

    def table_exists(self, table):
        """
        Checks if a table exists in Cassandra

        :param table: Target Cassandra table.
                      Use dot notation to target a specific keyspace.
        :type table: str
        """
        keyspace = self.keyspace
        if '.' in table:
            keyspace, table = table.split('.', 1)
        cluster_metadata = self.get_conn().cluster.metadata
        return keyspace in cluster_metadata.keyspaces and table in cluster_metadata.keyspaces[keyspace].tables

    def record_exists(self, table, keys):
        """
        Checks if a record exists in Cassandra

        :param table: Target Cassandra table.
                      Use dot notation to target a specific keyspace.
        :type table: str
        :param keys: The keys and their values to check the existence.
        :type keys: dict
        """
        keyspace = self.keyspace
        if '.' in table:
            keyspace, table = table.split('.', 1)
        ks = ' AND '.join('{}=%({})s'.format(key, key) for key in keys.keys())
        cql = 'SELECT * FROM {keyspace}.{table} WHERE {keys}'.format(keyspace=keyspace,
          table=table,
          keys=ks)
        try:
            rs = self.get_conn().execute(cql, keys)
            return rs.one() is not None
        except Exception:
            return False