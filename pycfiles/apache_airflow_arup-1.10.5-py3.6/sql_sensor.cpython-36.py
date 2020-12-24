# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Runs a sql statement repeatedly until a criteria is met. It will keep trying until\n    success or failure criteria are met, or if the first cell is in (0, '0', ''). Optional success\n    and failure callables are called with the first cell returned as the argument. If success\n    callable is defined the sensor will keep retrying until the criteria is met.\n    If failure callable is defined and the criteria is met the sensor will raise AirflowException.\n    Failure criteria is evaluated before success criteria. A fail_on_empty boolean can also\n    be passed to the sensor in which case it will fail if no rows have been returned\n\n    :param conn_id: The connection to run the sensor against\n    :type conn_id: str\n    :param sql: The sql to run. To pass, it needs to return at least one cell\n        that contains a non-zero / empty string value.\n    :type sql: str\n    :param parameters: The parameters to render the SQL query with (optional).\n    :type parameters: mapping or iterable\n    :param success: Success criteria for the sensor is a Callable that takes first_cell\n        as the only argument, and returns a boolean (optional).\n    :type: success: Optional<Callable[[Any], bool]>\n    :param failure: Failure criteria for the sensor is a Callable that takes first_cell\n        as the only argument and return a boolean (optional).\n    :type: failure: Optional<Callable[[Any], bool]>\n    :param fail_on_empty: Explicitly fail on no rows returned\n    :type: fail_on_empty: bool\n    "
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