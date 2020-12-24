# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/sql_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4806 bytes
from builtins import str
from typing import Iterable
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class SqlSensor(BaseSensorOperator):
    """SqlSensor"""
    template_fields = ('sql', )
    template_ext = ('.hql', '.sql')
    ui_color = '#7c7287'

    @apply_defaults
    def __init__(self, conn_id, sql, parameters=None, success=None, failure=None, fail_on_empty=False, *args, **kwargs):
        self.conn_id = conn_id
        self.sql = sql
        self.parameters = parameters
        self.success = success
        self.failure = failure
        self.fail_on_empty = fail_on_empty
        (super(SqlSensor, self).__init__)(*args, **kwargs)

    def poke(self, context):
        conn = BaseHook.get_connection(self.conn_id)
        allowed_conn_type = {
         'google_cloud_platform', 'jdbc', 'mssql',
         'mysql', 'oracle', 'postgres',
         'presto', 'sqlite', 'vertica'}
        if conn.conn_type not in allowed_conn_type:
            raise AirflowException('The connection type is not supported by SqlSensor. ' + 'Supported connection types: {}'.format(list(allowed_conn_type)))
        else:
            hook = conn.get_hook()
            self.log.info('Poking: %s (with parameters %s)', self.sql, self.parameters)
            records = hook.get_records(self.sql, self.parameters)
            if not records:
                if self.fail_on_empty:
                    raise AirflowException('No rows returned, raising as per fail_on_empty flag')
                else:
                    return False
        first_cell = records[0][0]
        if self.failure is not None:
            if callable(self.failure):
                if self.failure(first_cell):
                    raise AirflowException('Failure criteria met. self.failure({}) returned True'.format(first_cell))
            else:
                raise AirflowException('self.failure is present, but not callable -> {}'.format(self.success))
        if self.success is not None:
            if callable(self.success):
                return self.success(first_cell)
            raise AirflowException('self.success is present, but not callable -> {}'.format(self.success))
        return str(first_cell) not in ('0', '')