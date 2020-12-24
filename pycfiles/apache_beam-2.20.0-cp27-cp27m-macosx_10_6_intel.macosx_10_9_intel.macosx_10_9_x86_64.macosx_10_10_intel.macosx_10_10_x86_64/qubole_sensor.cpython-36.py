# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/qubole_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4083 bytes
from qds_sdk.qubole import Qubole
from qds_sdk.sensors import FileSensor, PartitionSensor
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class QuboleSensor(BaseSensorOperator):
    """QuboleSensor"""
    template_fields = ('data', 'qubole_conn_id')
    template_ext = ('.txt', )

    @apply_defaults
    def __init__(self, data, qubole_conn_id='qubole_default', *args, **kwargs):
        self.data = data
        self.qubole_conn_id = qubole_conn_id
        if 'poke_interval' in kwargs:
            if kwargs['poke_interval'] < 5:
                raise AirflowException("Sorry, poke_interval can't be less than 5 sec for task '{0}' in dag '{1}'.".format(kwargs['task_id'], kwargs['dag'].dag_id))
        (super(QuboleSensor, self).__init__)(*args, **kwargs)

    def poke(self, context):
        conn = BaseHook.get_connection(self.qubole_conn_id)
        Qubole.configure(api_token=(conn.password), api_url=(conn.host))
        self.log.info('Poking: %s', self.data)
        status = False
        try:
            status = self.sensor_class.check(self.data)
        except Exception as e:
            self.log.exception(e)
            status = False

        self.log.info('Status of this Poke: %s', status)
        return status


class QuboleFileSensor(QuboleSensor):
    """QuboleFileSensor"""

    @apply_defaults
    def __init__(self, *args, **kwargs):
        self.sensor_class = FileSensor
        (super(QuboleFileSensor, self).__init__)(*args, **kwargs)


class QubolePartitionSensor(QuboleSensor):
    """QubolePartitionSensor"""

    @apply_defaults
    def __init__(self, *args, **kwargs):
        self.sensor_class = PartitionSensor
        (super(QubolePartitionSensor, self).__init__)(*args, **kwargs)