# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/db.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 14180 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from functools import wraps
import os, contextlib
from airflow import settings
from airflow.configuration import conf
from airflow.utils.log.logging_mixin import LoggingMixin
log = LoggingMixin().log

@contextlib.contextmanager
def create_session():
    """
    Contextmanager that will create and teardown a session.
    """
    session = settings.Session()
    try:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise

    finally:
        session.close()


def provide_session(func):
    """
    Function decorator that provides a session if it isn't provided.
    If you want to reuse a session or run the function as part of a
    database transaction, you pass it to the function, if not this wrapper
    will create one and close it for you.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_session = 'session'
        func_params = func.__code__.co_varnames
        session_in_args = arg_session in func_params and func_params.index(arg_session) < len(args)
        session_in_kwargs = arg_session in kwargs
        if session_in_kwargs or session_in_args:
            return func(*args, **kwargs)
        with create_session() as (session):
            kwargs[arg_session] = session
            return func(*args, **kwargs)

    return wrapper


@provide_session
def merge_conn(conn, session=None):
    from airflow.models import Connection
    if not session.query(Connection).filter(Connection.conn_id == conn.conn_id).first():
        session.add(conn)
        session.commit()


@provide_session
def add_default_pool_if_not_exists(session=None):
    from airflow.models.pool import Pool
    if not Pool.get_pool((Pool.DEFAULT_POOL_NAME), session=session):
        default_pool = Pool(pool=(Pool.DEFAULT_POOL_NAME),
          slots=conf.getint(section='core', key='non_pooled_task_slot_count', fallback=128),
          description='Default pool')
        session.add(default_pool)
        session.commit()


def initdb(rbac=False):
    session = settings.Session()
    from airflow import models
    from airflow.models import Connection
    upgradedb()
    merge_conn(Connection(conn_id='airflow_db',
      conn_type='mysql',
      host='mysql',
      login='root',
      password='',
      schema='airflow'))
    merge_conn(Connection(conn_id='beeline_default',
      conn_type='beeline',
      port=10000,
      host='localhost',
      extra='{"use_beeline": true, "auth": ""}',
      schema='default'))
    merge_conn(Connection(conn_id='bigquery_default',
      conn_type='google_cloud_platform',
      schema='default'))
    merge_conn(Connection(conn_id='local_mysql',
      conn_type='mysql',
      host='localhost',
      login='airflow',
      password='airflow',
      schema='airflow'))
    merge_conn(Connection(conn_id='presto_default',
      conn_type='presto',
      host='localhost',
      schema='hive',
      port=3400))
    merge_conn(Connection(conn_id='google_cloud_default',
      conn_type='google_cloud_platform',
      schema='default'))
    merge_conn(Connection(conn_id='hive_cli_default',
      conn_type='hive_cli',
      schema='default'))
    merge_conn(Connection(conn_id='pig_cli_default',
      conn_type='pig_cli',
      schema='default'))
    merge_conn(Connection(conn_id='hiveserver2_default',
      conn_type='hiveserver2',
      host='localhost',
      schema='default',
      port=10000))
    merge_conn(Connection(conn_id='metastore_default',
      conn_type='hive_metastore',
      host='localhost',
      extra='{"authMechanism": "PLAIN"}',
      port=9083))
    merge_conn(Connection(conn_id='mongo_default',
      conn_type='mongo',
      host='mongo',
      port=27017))
    merge_conn(Connection(conn_id='mysql_default',
      conn_type='mysql',
      login='root',
      schema='airflow',
      host='mysql'))
    merge_conn(Connection(conn_id='postgres_default',
      conn_type='postgres',
      login='postgres',
      password='airflow',
      schema='airflow',
      host='postgres'))
    merge_conn(Connection(conn_id='sqlite_default',
      conn_type='sqlite',
      host='/tmp/sqlite_default.db'))
    merge_conn(Connection(conn_id='http_default',
      conn_type='http',
      host='https://www.google.com/'))
    merge_conn(Connection(conn_id='mssql_default',
      conn_type='mssql',
      host='localhost',
      port=1433))
    merge_conn(Connection(conn_id='vertica_default',
      conn_type='vertica',
      host='localhost',
      port=5433))
    merge_conn(Connection(conn_id='wasb_default',
      conn_type='wasb',
      extra='{"sas_token": null}'))
    merge_conn(Connection(conn_id='webhdfs_default',
      conn_type='hdfs',
      host='localhost',
      port=50070))
    merge_conn(Connection(conn_id='ssh_default',
      conn_type='ssh',
      host='localhost'))
    merge_conn(Connection(conn_id='sftp_default',
      conn_type='sftp',
      host='localhost',
      port=22,
      login='airflow',
      extra='\n                {"key_file": "~/.ssh/id_rsa", "no_host_key_check": true}\n            '))
    merge_conn(Connection(conn_id='fs_default',
      conn_type='fs',
      extra='{"path": "/"}'))
    merge_conn(Connection(conn_id='aws_default',
      conn_type='aws',
      extra='{"region_name": "us-east-1"}'))
    merge_conn(Connection(conn_id='spark_default',
      conn_type='spark',
      host='yarn',
      extra='{"queue": "root.default"}'))
    merge_conn(Connection(conn_id='druid_broker_default',
      conn_type='druid',
      host='druid-broker',
      port=8082,
      extra='{"endpoint": "druid/v2/sql"}'))
    merge_conn(Connection(conn_id='druid_ingest_default',
      conn_type='druid',
      host='druid-overlord',
      port=8081,
      extra='{"endpoint": "druid/indexer/v1/task"}'))
    merge_conn(Connection(conn_id='redis_default',
      conn_type='redis',
      host='redis',
      port=6379,
      extra='{"db": 0}'))
    merge_conn(Connection(conn_id='sqoop_default',
      conn_type='sqoop',
      host='rmdbs',
      extra=''))
    merge_conn(Connection(conn_id='emr_default',
      conn_type='emr',
      extra='\n                {   "Name": "default_job_flow_name",\n                    "LogUri": "s3://my-emr-log-bucket/default_job_flow_location",\n                    "ReleaseLabel": "emr-4.6.0",\n                    "Instances": {\n                        "Ec2KeyName": "mykey",\n                        "Ec2SubnetId": "somesubnet",\n                        "InstanceGroups": [\n                            {\n                                "Name": "Master nodes",\n                                "Market": "ON_DEMAND",\n                                "InstanceRole": "MASTER",\n                                "InstanceType": "r3.2xlarge",\n                                "InstanceCount": 1\n                            },\n                            {\n                                "Name": "Slave nodes",\n                                "Market": "ON_DEMAND",\n                                "InstanceRole": "CORE",\n                                "InstanceType": "r3.2xlarge",\n                                "InstanceCount": 1\n                            }\n                        ],\n                        "TerminationProtected": false,\n                        "KeepJobFlowAliveWhenNoSteps": false\n                    },\n                    "Applications":[\n                        { "Name": "Spark" }\n                    ],\n                    "VisibleToAllUsers": true,\n                    "JobFlowRole": "EMR_EC2_DefaultRole",\n                    "ServiceRole": "EMR_DefaultRole",\n                    "Tags": [\n                        {\n                            "Key": "app",\n                            "Value": "analytics"\n                        },\n                        {\n                            "Key": "environment",\n                            "Value": "development"\n                        }\n                    ]\n                }\n            '))
    merge_conn(Connection(conn_id='databricks_default',
      conn_type='databricks',
      host='localhost'))
    merge_conn(Connection(conn_id='qubole_default',
      conn_type='qubole',
      host='localhost'))
    (
     merge_conn(Connection(conn_id='segment_default',
       conn_type='segment',
       extra='{"write_key": "my-segment-write-key"}')),)
    merge_conn(Connection(conn_id='azure_data_lake_default',
      conn_type='azure_data_lake',
      extra='{"tenant": "<TENANT>", "account_name": "<ACCOUNTNAME>" }'))
    merge_conn(Connection(conn_id='azure_cosmos_default',
      conn_type='azure_cosmos',
      extra='{"database_name": "<DATABASE_NAME>", "collection_name": "<COLLECTION_NAME>" }'))
    merge_conn(Connection(conn_id='azure_container_instances_default',
      conn_type='azure_container_instances',
      extra='{"tenantId": "<TENANT>", "subscriptionId": "<SUBSCRIPTION ID>" }'))
    merge_conn(Connection(conn_id='cassandra_default',
      conn_type='cassandra',
      host='cassandra',
      port=9042))
    merge_conn(Connection(conn_id='dingding_default',
      conn_type='http',
      host='',
      password=''))
    merge_conn(Connection(conn_id='opsgenie_default',
      conn_type='http',
      host='',
      password=''))
    KET = models.KnownEventType
    if not session.query(KET).filter(KET.know_event_type == 'Holiday').first():
        session.add(KET(know_event_type='Holiday'))
    if not session.query(KET).filter(KET.know_event_type == 'Outage').first():
        session.add(KET(know_event_type='Outage'))
    if not session.query(KET).filter(KET.know_event_type == 'Natural Disaster').first():
        session.add(KET(know_event_type='Natural Disaster'))
    if not session.query(KET).filter(KET.know_event_type == 'Marketing Campaign').first():
        session.add(KET(know_event_type='Marketing Campaign'))
    session.commit()
    dagbag = models.DagBag()
    for dag in dagbag.dags.values():
        dag.sync_to_db()

    models.DAG.deactivate_unknown_dags(dagbag.dags.keys())
    Chart = models.Chart
    chart_label = 'Airflow task instance by type'
    chart = session.query(Chart).filter(Chart.label == chart_label).first()
    if not chart:
        chart = Chart(label=chart_label,
          conn_id='airflow_db',
          chart_type='bar',
          x_is_date=False,
          sql="SELECT state, COUNT(1) as number FROM task_instance WHERE dag_id LIKE 'example%' GROUP BY state")
        session.add(chart)
        session.commit()
    if rbac:
        from flask_appbuilder.security.sqla import models
        from flask_appbuilder.models.sqla import Base
        Base.metadata.create_all(settings.engine)


def upgradedb():
    from alembic import command
    from alembic.config import Config
    log.info('Creating tables')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    package_dir = os.path.normpath(os.path.join(current_dir, '..'))
    directory = os.path.join(package_dir, 'migrations')
    config = Config(os.path.join(package_dir, 'alembic.ini'))
    config.set_main_option('script_location', directory.replace('%', '%%'))
    config.set_main_option('sqlalchemy.url', settings.SQL_ALCHEMY_CONN.replace('%', '%%'))
    command.upgrade(config, 'heads')
    add_default_pool_if_not_exists()


def resetdb(rbac):
    """
    Clear out the database
    """
    from airflow import models
    from alembic.migration import MigrationContext
    log.info('Dropping tables that exist')
    connection = settings.engine.connect()
    models.base.Base.metadata.drop_all(connection)
    mc = MigrationContext.configure(connection)
    if mc._version.exists(connection):
        mc._version.drop(connection)
    if rbac:
        from flask_appbuilder.security.sqla import models
        from flask_appbuilder.models.sqla import Base
        Base.metadata.drop_all(connection)
    from flask_appbuilder.models.sqla import Base
    Base.metadata.drop_all(connection)
    initdb(rbac)