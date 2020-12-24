# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/hive_to_druid.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9654 bytes
from airflow.hooks.hive_hooks import HiveCliHook, HiveMetastoreHook
from airflow.hooks.druid_hook import DruidHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
LOAD_CHECK_INTERVAL = 5
DEFAULT_TARGET_PARTITION_SIZE = 5000000

class HiveToDruidTransfer(BaseOperator):
    """HiveToDruidTransfer"""
    template_fields = ('sql', 'intervals')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, sql, druid_datasource, ts_dim, metric_spec=None, hive_cli_conn_id='hive_cli_default', druid_ingest_conn_id='druid_ingest_default', metastore_conn_id='metastore_default', hadoop_dependency_coordinates=None, intervals=None, num_shards=-1, target_partition_size=-1, query_granularity='NONE', segment_granularity='DAY', hive_tblproperties=None, job_properties=None, *args, **kwargs):
        (super(HiveToDruidTransfer, self).__init__)(*args, **kwargs)
        self.sql = sql
        self.druid_datasource = druid_datasource
        self.ts_dim = ts_dim
        self.intervals = intervals or ['{{ ds }}/{{ tomorrow_ds }}']
        self.num_shards = num_shards
        self.target_partition_size = target_partition_size
        self.query_granularity = query_granularity
        self.segment_granularity = segment_granularity
        self.metric_spec = metric_spec or [
         {'name':'count', 
          'type':'count'}]
        self.hive_cli_conn_id = hive_cli_conn_id
        self.hadoop_dependency_coordinates = hadoop_dependency_coordinates
        self.druid_ingest_conn_id = druid_ingest_conn_id
        self.metastore_conn_id = metastore_conn_id
        self.hive_tblproperties = hive_tblproperties or {}
        self.job_properties = job_properties

    def execute(self, context):
        hive = HiveCliHook(hive_cli_conn_id=(self.hive_cli_conn_id))
        self.log.info('Extracting data from Hive')
        hive_table = 'druid.' + context['task_instance_key_str'].replace('.', '_')
        sql = self.sql.strip().strip(';')
        tblproperties = ''.join([", '{}' = '{}'".format(k, v) for k, v in self.hive_tblproperties.items()])
        hql = "        SET mapred.output.compress=false;\n        SET hive.exec.compress.output=false;\n        DROP TABLE IF EXISTS {hive_table};\n        CREATE TABLE {hive_table}\n        ROW FORMAT DELIMITED FIELDS TERMINATED BY '\t'\n        STORED AS TEXTFILE\n        TBLPROPERTIES ('serialization.null.format' = ''{tblproperties})\n        AS\n        {sql}\n        ".format(hive_table=hive_table, tblproperties=tblproperties, sql=sql)
        self.log.info('Running command:\n %s', hql)
        hive.run_cli(hql)
        m = HiveMetastoreHook(self.metastore_conn_id)
        t = m.get_table(hive_table)
        columns = [col.name for col in t.sd.cols]
        hdfs_uri = m.get_table(hive_table).sd.location
        pos = hdfs_uri.find('/user')
        static_path = hdfs_uri[pos:]
        schema, table = hive_table.split('.')
        druid = DruidHook(druid_ingest_conn_id=(self.druid_ingest_conn_id))
        try:
            index_spec = self.construct_ingest_query(static_path=static_path,
              columns=columns)
            self.log.info('Inserting rows into Druid, hdfs path: %s', static_path)
            druid.submit_indexing_job(index_spec)
            self.log.info('Load seems to have succeeded!')
        finally:
            self.log.info('Cleaning up by dropping the temp Hive table %s', hive_table)
            hql = 'DROP TABLE IF EXISTS {}'.format(hive_table)
            hive.run_cli(hql)

    def construct_ingest_query(self, static_path, columns):
        """
        Builds an ingest query for an HDFS TSV load.

        :param static_path: The path on hdfs where the data is
        :type static_path: str
        :param columns: List of all the columns that are available
        :type columns: list
        """
        num_shards = self.num_shards
        target_partition_size = self.target_partition_size
        if self.target_partition_size == -1:
            if self.num_shards == -1:
                target_partition_size = DEFAULT_TARGET_PARTITION_SIZE
        else:
            num_shards = -1
        metric_names = [m['fieldName'] for m in self.metric_spec if m['type'] != 'count']
        dimensions = [c for c in columns if c not in metric_names if c != self.ts_dim]
        ingest_query_dict = {'type':'index_hadoop', 
         'spec':{'dataSchema':{'metricsSpec':self.metric_spec, 
           'granularitySpec':{'queryGranularity':self.query_granularity, 
            'intervals':self.intervals, 
            'type':'uniform', 
            'segmentGranularity':self.segment_granularity}, 
           'parser':{'type':'string', 
            'parseSpec':{'columns':columns, 
             'dimensionsSpec':{'dimensionExclusions':[],  'dimensions':dimensions, 
              'spatialDimensions':[]}, 
             'timestampSpec':{'column':self.ts_dim, 
              'format':'auto'}, 
             'format':'tsv'}}, 
           'dataSource':self.druid_datasource}, 
          'tuningConfig':{'type':'hadoop', 
           'jobProperties':{'mapreduce.job.user.classpath.first':'false', 
            'mapreduce.map.output.compress':'false', 
            'mapreduce.output.fileoutputformat.compress':'false'}, 
           'partitionsSpec':{'type':'hashed', 
            'targetPartitionSize':target_partition_size, 
            'numShards':num_shards}}, 
          'ioConfig':{'inputSpec':{'paths':static_path, 
            'type':'static'}, 
           'type':'hadoop'}}}
        if self.job_properties:
            ingest_query_dict['spec']['tuningConfig']['jobProperties'].update(self.job_properties)
        if self.hadoop_dependency_coordinates:
            ingest_query_dict['hadoopDependencyCoordinates'] = self.hadoop_dependency_coordinates
        return ingest_query_dict