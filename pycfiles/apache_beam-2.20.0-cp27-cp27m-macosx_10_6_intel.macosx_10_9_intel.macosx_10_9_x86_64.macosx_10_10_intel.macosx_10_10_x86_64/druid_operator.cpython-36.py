# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/druid_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2283 bytes
import json
from airflow.hooks.druid_hook import DruidHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DruidOperator(BaseOperator):
    """DruidOperator"""
    template_fields = ('index_spec_str', )
    template_ext = ('.json', )

    @apply_defaults
    def __init__(self, json_index_file, druid_ingest_conn_id='druid_ingest_default', max_ingestion_time=None, *args, **kwargs):
        (super(DruidOperator, self).__init__)(*args, **kwargs)
        self.conn_id = druid_ingest_conn_id
        self.max_ingestion_time = max_ingestion_time
        with open(json_index_file) as (data_file):
            index_spec = json.load(data_file)
        self.index_spec_str = json.dumps(index_spec,
          sort_keys=True,
          indent=4,
          separators=(',', ': '))

    def execute(self, context):
        hook = DruidHook(druid_ingest_conn_id=(self.conn_id),
          max_ingestion_time=(self.max_ingestion_time))
        self.log.info('Submitting %s', self.index_spec_str)
        hook.submit_indexing_job(self.index_spec_str)