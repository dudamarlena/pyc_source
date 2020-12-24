# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/redshift_to_s3_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6486 bytes
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class RedshiftToS3Transfer(BaseOperator):
    __doc__ = '\n    Executes an UNLOAD command to s3 as a CSV with headers\n\n    :param schema: reference to a specific schema in redshift database\n    :type schema: str\n    :param table: reference to a specific table in redshift database\n    :type table: str\n    :param s3_bucket: reference to a specific S3 bucket\n    :type s3_bucket: str\n    :param s3_key: reference to a specific S3 key\n    :type s3_key: str\n    :param redshift_conn_id: reference to a specific redshift database\n    :type redshift_conn_id: str\n    :param aws_conn_id: reference to a specific S3 connection\n    :type aws_conn_id: str\n    :param verify: Whether or not to verify SSL certificates for S3 connection.\n        By default SSL certificates are verified.\n        You can provide the following values:\n\n        - ``False``: do not validate SSL certificates. SSL will still be used\n                 (unless use_ssl is False), but SSL certificates will not be\n                 verified.\n        - ``path/to/cert/bundle.pem``: A filename of the CA cert bundle to uses.\n                 You can specify this argument if you want to use a different\n                 CA cert bundle than the one used by botocore.\n    :type verify: bool or str\n    :param unload_options: reference to a list of UNLOAD options\n    :type unload_options: list\n    '
    template_fields = ()
    template_ext = ()
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, schema, table, s3_bucket, s3_key, redshift_conn_id='redshift_default', aws_conn_id='aws_default', verify=None, unload_options=tuple(), autocommit=False, include_header=False, *args, **kwargs):
        (super(RedshiftToS3Transfer, self).__init__)(*args, **kwargs)
        self.schema = schema
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.verify = verify
        self.unload_options = unload_options
        self.autocommit = autocommit
        self.include_header = include_header
        if self.include_header:
            if 'PARALLEL OFF' not in [uo.upper().strip() for uo in unload_options]:
                self.unload_options = list(unload_options) + ['PARALLEL OFF']

    def execute(self, context):
        self.hook = PostgresHook(postgres_conn_id=(self.redshift_conn_id))
        self.s3 = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        credentials = self.s3.get_credentials()
        unload_options = '\n\t\t\t'.join(self.unload_options)
        if self.include_header:
            self.log.info('Retrieving headers from %s.%s...', self.schema, self.table)
            columns_query = "SELECT column_name\n                                        FROM information_schema.columns\n                                        WHERE table_schema = '{schema}'\n                                        AND   table_name = '{table}'\n                                        ORDER BY ordinal_position\n                            ".format(schema=(self.schema), table=(self.table))
            cursor = self.hook.get_conn().cursor()
            cursor.execute(columns_query)
            rows = cursor.fetchall()
            columns = [row[0] for row in rows]
            column_names = ', '.join('{0}'.format(c) for c in columns)
            column_headers = ', '.join("\\'{0}\\'".format(c) for c in columns)
            column_castings = ', '.join('CAST({0} AS text) AS {0}'.format(c) for c in columns)
            select_query = 'SELECT {column_names} FROM\n                                    (SELECT 2 sort_order, {column_castings}\n                                     FROM {schema}.{table}\n                                    UNION ALL\n                                    SELECT 1 sort_order, {column_headers})\n                                 ORDER BY sort_order'.format(column_names=column_names,
              column_castings=column_castings,
              column_headers=column_headers,
              schema=(self.schema),
              table=(self.table))
        else:
            select_query = 'SELECT * FROM {schema}.{table}'.format(schema=(self.schema),
              table=(self.table))
        unload_query = "\n                    UNLOAD ('{select_query}')\n                    TO 's3://{s3_bucket}/{s3_key}/{table}_'\n                    with credentials\n                    'aws_access_key_id={access_key};aws_secret_access_key={secret_key}'\n                    {unload_options};\n                    ".format(select_query=select_query, table=(self.table),
          s3_bucket=(self.s3_bucket),
          s3_key=(self.s3_key),
          access_key=(credentials.access_key),
          secret_key=(credentials.secret_key),
          unload_options=unload_options)
        self.log.info('Executing UNLOAD command...')
        self.hook.run(unload_query, self.autocommit)
        self.log.info('UNLOAD command complete...')