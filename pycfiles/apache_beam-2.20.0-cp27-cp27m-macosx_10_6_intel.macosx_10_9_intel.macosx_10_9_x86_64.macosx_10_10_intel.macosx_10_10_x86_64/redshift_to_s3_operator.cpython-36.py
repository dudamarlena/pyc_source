# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/redshift_to_s3_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6486 bytes
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class RedshiftToS3Transfer(BaseOperator):
    """RedshiftToS3Transfer"""
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