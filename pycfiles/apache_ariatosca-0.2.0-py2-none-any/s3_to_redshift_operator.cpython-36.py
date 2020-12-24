# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/s3_to_redshift_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4223 bytes
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class S3ToRedshiftTransfer(BaseOperator):
    """S3ToRedshiftTransfer"""
    template_fields = ()
    template_ext = ()
    ui_color = '#ededed'

    @apply_defaults
    def __init__(self, schema, table, s3_bucket, s3_key, redshift_conn_id='redshift_default', aws_conn_id='aws_default', verify=None, copy_options=tuple(), autocommit=False, parameters=None, *args, **kwargs):
        (super(S3ToRedshiftTransfer, self).__init__)(*args, **kwargs)
        self.schema = schema
        self.table = table
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.redshift_conn_id = redshift_conn_id
        self.aws_conn_id = aws_conn_id
        self.verify = verify
        self.copy_options = copy_options
        self.autocommit = autocommit
        self.parameters = parameters

    def execute(self, context):
        self.hook = PostgresHook(postgres_conn_id=(self.redshift_conn_id))
        self.s3 = S3Hook(aws_conn_id=(self.aws_conn_id), verify=(self.verify))
        credentials = self.s3.get_credentials()
        copy_options = '\n\t\t\t'.join(self.copy_options)
        copy_query = "\n            COPY {schema}.{table}\n            FROM 's3://{s3_bucket}/{s3_key}/{table}'\n            with credentials\n            'aws_access_key_id={access_key};aws_secret_access_key={secret_key}'\n            {copy_options};\n        ".format(schema=(self.schema), table=(self.table),
          s3_bucket=(self.s3_bucket),
          s3_key=(self.s3_key),
          access_key=(credentials.access_key),
          secret_key=(credentials.secret_key),
          copy_options=copy_options)
        self.log.info('Executing COPY command...')
        self.hook.run(copy_query, self.autocommit)
        self.log.info('COPY command complete...')