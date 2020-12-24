# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/postgres_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6411 bytes
import os, psycopg2, psycopg2.extensions
from contextlib import closing
from airflow.hooks.dbapi_hook import DbApiHook

class PostgresHook(DbApiHook):
    __doc__ = '\n    Interact with Postgres.\n    You can specify ssl parameters in the extra field of your connection\n    as ``{"sslmode": "require", "sslcert": "/path/to/cert.pem", etc}``.\n\n    Note: For Redshift, use keepalives_idle in the extra connection parameters\n    and set it to less than 300 seconds.\n\n    Note: For AWS IAM authentication, use iam in the extra connection parameters\n    and set it to true. Leave the password field empty. This will use the the\n    "aws_default" connection to get the temporary token unless you override\n    in extras.\n    extras example: ``{"iam":true, "aws_conn_id":"my_aws_conn"}``\n    For Redshift, also use redshift in the extra connection parameters and\n    set it to true. The cluster-identifier is extracted from the beginning of\n    the host field, so is optional. It can however be overridden in the extra field.\n    extras example: ``{"iam":true, "redshift":true, "cluster-identifier": "my_cluster_id"}``\n    '
    conn_name_attr = 'postgres_conn_id'
    default_conn_name = 'postgres_default'
    supports_autocommit = True

    def __init__(self, *args, **kwargs):
        (super(PostgresHook, self).__init__)(*args, **kwargs)
        self.schema = kwargs.pop('schema', None)

    def get_conn(self):
        conn = self.get_connection(self.postgres_conn_id)
        if conn.extra_dejson.get('iam', False):
            conn.login, conn.password, conn.port = self.get_iam_token(conn)
        conn_args = dict(host=(conn.host),
          user=(conn.login),
          password=(conn.password),
          dbname=(self.schema or conn.schema),
          port=(conn.port))
        for arg_name, arg_val in conn.extra_dejson.items():
            if arg_name in ('sslmode', 'sslcert', 'sslkey', 'sslrootcert', 'sslcrl',
                            'application_name', 'keepalives_idle'):
                conn_args[arg_name] = arg_val

        self.conn = (psycopg2.connect)(**conn_args)
        return self.conn

    def copy_expert(self, sql, filename, open=open):
        """
        Executes SQL using psycopg2 copy_expert method.
        Necessary to execute COPY command without access to a superuser.

        Note: if this method is called with a "COPY FROM" statement and
        the specified input file does not exist, it creates an empty
        file and no data is loaded, but the operation succeeds.
        So if users want to be aware when the input file does not exist,
        they have to check its existence by themselves.
        """
        if not os.path.isfile(filename):
            with open(filename, 'w'):
                pass
        with open(filename, 'r+') as (f):
            with closing(self.get_conn()) as (conn):
                with closing(conn.cursor()) as (cur):
                    cur.copy_expert(sql, f)
                    f.truncate(f.tell())
                    conn.commit()

    def bulk_load(self, table, tmp_file):
        """
        Loads a tab-delimited file into a database table
        """
        self.copy_expert('COPY {table} FROM STDIN'.format(table=table), tmp_file)

    def bulk_dump(self, table, tmp_file):
        """
        Dumps a database table into a tab-delimited file
        """
        self.copy_expert('COPY {table} TO STDOUT'.format(table=table), tmp_file)

    @staticmethod
    def _serialize_cell(cell, conn):
        """
        Postgresql will adapt all arguments to the execute() method internally,
        hence we return cell without any conversion.

        See http://initd.org/psycopg/docs/advanced.html#adapting-new-types for
        more information.

        :param cell: The cell to insert into the table
        :type cell: object
        :param conn: The database connection
        :type conn: connection object
        :return: The cell
        :rtype: object
        """
        return cell

    def get_iam_token(self, conn):
        """
        Uses AWSHook to retrieve a temporary password to connect to Postgres
        or Redshift. Port is required. If none is provided, default is used for
        each service
        """
        from airflow.contrib.hooks.aws_hook import AwsHook
        redshift = conn.extra_dejson.get('redshift', False)
        aws_conn_id = conn.extra_dejson.get('aws_conn_id', 'aws_default')
        aws_hook = AwsHook(aws_conn_id)
        login = conn.login
        if conn.port is None:
            port = 5439 if redshift else 5432
        else:
            port = conn.port
        if redshift:
            cluster_identifier = conn.extra_dejson.get('cluster-identifier', conn.host.split('.')[0])
            client = aws_hook.get_client_type('redshift')
            cluster_creds = client.get_cluster_credentials(DbUser=(conn.login),
              DbName=(self.schema or conn.schema),
              ClusterIdentifier=cluster_identifier,
              AutoCreate=False)
            token = cluster_creds['DbPassword']
            login = cluster_creds['DbUser']
        else:
            client = aws_hook.get_client_type('rds')
            token = client.generate_db_auth_token(conn.host, port, conn.login)
        return (
         login, token, port)