# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/sensors.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2753 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator as BaseSensorOperatorImp
from airflow.sensors.external_task_sensor import ExternalTaskSensor as ExternalTaskSensorImp
from airflow.sensors.hdfs_sensor import HdfsSensor as HdfsSensorImp
from airflow.sensors.hive_partition_sensor import HivePartitionSensor as HivePartitionSensorImp
from airflow.sensors.http_sensor import HttpSensor as HttpSensorImp
from airflow.sensors.metastore_partition_sensor import MetastorePartitionSensor as MetastorePartitionSensorImp
from airflow.sensors.s3_key_sensor import S3KeySensor as S3KeySensorImp
from airflow.sensors.s3_prefix_sensor import S3PrefixSensor as S3PrefixSensorImp
from airflow.sensors.sql_sensor import SqlSensor as SqlSensorImp
from airflow.sensors.time_delta_sensor import TimeDeltaSensor as TimeDeltaSensorImp
from airflow.sensors.time_sensor import TimeSensor as TimeSensorImp
from airflow.sensors.web_hdfs_sensor import WebHdfsSensor as WebHdfsSensorImp

class BaseSensorOperator(BaseSensorOperatorImp):
    pass


class ExternalTaskSensor(ExternalTaskSensorImp):
    pass


class HdfsSensor(HdfsSensorImp):
    pass


class HttpSensor(HttpSensorImp):
    pass


class MetastorePartitionSensor(MetastorePartitionSensorImp):
    pass


class HivePartitionSensor(HivePartitionSensorImp):
    pass


class S3KeySensor(S3KeySensorImp):
    pass


class S3PrefixSensor(S3PrefixSensorImp):
    pass


class SqlSensor(SqlSensorImp):
    pass


class TimeDeltaSensor(TimeDeltaSensorImp):
    pass


class TimeSensor(TimeSensorImp):
    pass


class WebHdfsSensor(WebHdfsSensorImp):
    pass