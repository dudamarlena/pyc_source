# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/alanjds/src/git/adwords-client/adwords_client/mappers/redshift.py
# Compiled at: 2017-07-12 10:46:26
# Size of source mod 2**32: 6013 bytes
import logging, os, tempfile, boto3, pandas as pd
from sqlalchemy import text
from sqlalchemy.types import String
logger = logging.getLogger(__name__)

class RedshiftMapper:

    def __init__(self, table_mappings, schema, connection_factory, bucket, aws_acc, aws_role_name):
        self.table_mappings = table_mappings
        self.schema = schema
        self.pg_engine = None
        self.bucket = bucket
        self.connection_factory = connection_factory
        self.aws_acc = aws_acc
        self.aws_role_name = aws_role_name
        self.lock = None

    def set_lock(self, lock):
        self.lock = lock

    def get_engine(self):
        if not self.pg_engine:
            self.pg_engine = self.connection_factory()
        return self.pg_engine

    def map_data(self, client, table_name, group_id, n_groups):
        full_table_name = '{}.{}'.format(self.schema, table_name)
        if self.table_mappings:
            if 'campaign_id' in self.table_mappings:
                query_fields = ','.join(field for field in self.table_mappings.values())
                query = text('select {} from {} where {}::int %% {} = {}'.format(query_fields, full_table_name, self.table_mappings['campaign_id'], n_groups, group_id))
        else:
            if n_groups > 1:
                logger.warning('"campaing_id" field not in table, can not automatically split data, reading full data in all workers')
            query = 'select * from {}'.format(full_table_name)
        df = pd.read_sql(query, self.get_engine())
        if self.table_mappings:
            df.rename(columns={value:key for key, value in self.table_mappings.items()}, inplace=True)
        df.to_sql(table_name, (client.engine), if_exists='replace', index=False)

    def upsync(self, client, source_table, target_table, drop_table=False):
        self.sqlite_to_redshift((client.engine), source_table,
          ('{}.{}'.format(self.schema, target_table)),
          drop_table=drop_table)

    def sqlite_to_redshift(self, sqlite_conn, from_table, to_table, drop_table=True):
        logger.info('Reading source table...')
        try:
            df = pd.read_sql_table(from_table, sqlite_conn)
            self.dataframe_to_redshift(df, to_table, drop_table)
        except ValueError:
            logger.error('Sqlite table {} does not exist...'.format(from_table))

    def upload_file_to_bucket(self, from_file, dry_run=False):
        logger.debug('Uploading {} to S3 (dry_run={})...'.format(from_file, str(dry_run)))
        remote_temp = os.path.basename(from_file)
        if not dry_run:
            cli = boto3.client('s3')
            cli.upload_file(from_file, self.bucket, remote_temp)
        return remote_temp

    def dataframe_to_redshift(self, df, to_table, drop_table=True):
        with tempfile.NamedTemporaryFile(delete=False) as (temp_file):
            temp_file_name = temp_file.name
        logger.info('Generating temporary compressed csv...')
        df.to_csv(temp_file_name, index=False,
          encoding='utf-8',
          compression='gzip',
          header=False)
        remote_temp = self.upload_file_to_bucket(temp_file_name)
        try:
            if drop_table:
                logger.info('Dropping destination table...')
                with self.lock:
                    with self.get_engine().begin() as (conn):
                        conn.execute('DROP TABLE IF EXISTS {}'.format(to_table))
            logger.info('Creating destination table...')
            dtype = dict((u, String(65535)) for u in dict(df.dtypes[(df.dtypes == 'object')]))
            query = pd.io.sql.get_schema(df, to_table, con=(self.get_engine()), dtype=dtype)
            query = query.replace('"', '').replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
            with self.lock:
                with self.get_engine().begin() as (conn):
                    conn.execute(query)
            fields = list(df.columns)
            self.csv_to_redshift(temp_file_name, to_table,
              fields,
              in_bucket=True)
        except Exception as e:
            if drop_table:
                logger.error('Table was set to be droppped, but an error ocurred:\n\n\t"{}"\n\nThe temporary file containing the data is written in\n\n\t{}.{}\n\nCheck the destination table\n\n\t{}\n\nAnd manually copy the CSV if necessary.'.format(str(e), self.bucket, remote_temp, to_table))
            raise e

        os.remove(temp_file_name)

    def csv_to_redshift(self, from_file, to_table, fields, in_bucket=False):
        remote_temp = self.upload_file_to_bucket(from_file, dry_run=in_bucket)
        logger.info('Copying data...')
        fields_string = ','.join(fields)
        query = "\n        copy {}({}) from 's3://{}/{}'\n        iam_role 'arn:aws:iam::{}:role/{}'\n        CSV\n        EMPTYASNULL\n        GZIP\n        ".format(to_table, fields_string, self.bucket, remote_temp, self.aws_acc, self.aws_role_name)
        with self.get_engine().begin() as (conn):
            conn.execute(query)
        cli = boto3.client('s3')
        cli.delete_object(Bucket=(self.bucket), Key=remote_temp)