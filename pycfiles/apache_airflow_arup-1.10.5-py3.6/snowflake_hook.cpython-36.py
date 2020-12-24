# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/snowflake_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5144 bytes
import snowflake.connector
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from airflow.hooks.dbapi_hook import DbApiHook

class SnowflakeHook(DbApiHook):
    __doc__ = '\n    Interact with Snowflake.\n\n    get_sqlalchemy_engine() depends on snowflake-sqlalchemy\n\n    '
    conn_name_attr = 'snowflake_conn_id'
    default_conn_name = 'snowflake_default'
    supports_autocommit = True

    def __init__(self, *args, **kwargs):
        (super(SnowflakeHook, self).__init__)(*args, **kwargs)
        self.account = kwargs.pop('account', None)
        self.warehouse = kwargs.pop('warehouse', None)
        self.database = kwargs.pop('database', None)
        self.region = kwargs.pop('region', None)
        self.role = kwargs.pop('role', None)
        self.schema = kwargs.pop('schema', None)

    def _get_conn_params(self):
        """
        one method to fetch connection params as a dict
        used in get_uri() and get_connection()
        """
        conn = self.get_connection(self.snowflake_conn_id)
        account = conn.extra_dejson.get('account', None)
        warehouse = conn.extra_dejson.get('warehouse', None)
        database = conn.extra_dejson.get('database', None)
        region = conn.extra_dejson.get('region', None)
        role = conn.extra_dejson.get('role', None)
        conn_config = {'user':conn.login, 
         'password':conn.password or '', 
         'schema':self.schema or conn.schema or '', 
         'database':self.database or database or '', 
         'account':self.account or account or '', 
         'warehouse':self.warehouse or warehouse or '', 
         'region':self.region or region or '', 
         'role':self.role or role or ''}
        private_key_file = conn.extra_dejson.get('private_key_file', None)
        if private_key_file:
            with open(private_key_file, 'rb') as (key):
                passphrase = None
                if conn.password:
                    passphrase = conn.password.strip().encode()
                p_key = serialization.load_pem_private_key((key.read()),
                  password=passphrase,
                  backend=(default_backend()))
            pkb = p_key.private_bytes(encoding=(serialization.Encoding.DER), format=(serialization.PrivateFormat.PKCS8),
              encryption_algorithm=(serialization.NoEncryption()))
            conn_config['private_key'] = pkb
            conn_config.pop('password', None)
        return conn_config

    def get_uri(self):
        """
        override DbApiHook get_uri method for get_sqlalchemy_engine()
        """
        conn_config = self._get_conn_params()
        uri = 'snowflake://{user}:{password}@{account}/{database}/'
        uri += '{schema}?warehouse={warehouse}&role={role}'
        return (uri.format)(**conn_config)

    def get_conn(self):
        """
        Returns a snowflake.connection object
        """
        conn_config = self._get_conn_params()
        conn = (snowflake.connector.connect)(**conn_config)
        return conn

    def _get_aws_credentials(self):
        """
        returns aws_access_key_id, aws_secret_access_key
        from extra

        intended to be used by external import and export statements
        """
        if self.snowflake_conn_id:
            connection_object = self.get_connection(self.snowflake_conn_id)
            if 'aws_secret_access_key' in connection_object.extra_dejson:
                aws_access_key_id = connection_object.extra_dejson.get('aws_access_key_id')
                aws_secret_access_key = connection_object.extra_dejson.get('aws_secret_access_key')
        return (
         aws_access_key_id, aws_secret_access_key)

    def set_autocommit(self, conn, autocommit):
        conn.autocommit(autocommit)