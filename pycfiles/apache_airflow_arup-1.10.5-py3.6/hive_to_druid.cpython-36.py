# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Moves data from Hive to Druid, [del]note that for now the data is loaded\n    into memory before being pushed to Druid, so this operator should\n    be used for smallish amount of data.[/del]\n\n    :param sql: SQL query to execute against the Druid database. (templated)\n    :type sql: str\n    :param druid_datasource: the datasource you want to ingest into in druid\n    :type druid_datasource: str\n    :param ts_dim: the timestamp dimension\n    :type ts_dim: str\n    :param metric_spec: the metrics you want to define for your data\n    :type metric_spec: list\n    :param hive_cli_conn_id: the hive connection id\n    :type hive_cli_conn_id: str\n    :param druid_ingest_conn_id: the druid ingest connection id\n    :type druid_ingest_conn_id: str\n    :param metastore_conn_id: the metastore connection id\n    :type metastore_conn_id: str\n    :param hadoop_dependency_coordinates: list of coordinates to squeeze\n        int the ingest json\n    :type hadoop_dependency_coordinates: list[str]\n    :param intervals: list of time intervals that defines segments,\n        this is passed as is to the json object. (templated)\n    :type intervals: list\n    :param hive_tblproperties: additional properties for tblproperties in\n        hive for the staging table\n    :type hive_tblproperties: dict\n    :param job_properties: additional properties for job\n    :type job_properties: dict\n    '
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