# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = '\n    Base class for all Qubole Sensors\n    '
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
    __doc__ = '\n    Wait for a file or folder to be present in cloud storage\n    and check for its presence via QDS APIs\n\n    :param qubole_conn_id: Connection id which consists of qds auth_token\n    :type qubole_conn_id: str\n    :param data: a JSON object containing payload, whose presence needs to be checked\n        Check this `example <https://github.com/apache/airflow/blob/master        /airflow/contrib/example_dags/example_qubole_sensor.py>`_ for sample payload\n        structure.\n    :type data: a JSON object\n\n    .. note:: Both ``data`` and ``qubole_conn_id`` fields support templating. You can\n        also use ``.txt`` files for template-driven use cases.\n    '

    @apply_defaults
    def __init__(self, *args, **kwargs):
        self.sensor_class = FileSensor
        (super(QuboleFileSensor, self).__init__)(*args, **kwargs)


class QubolePartitionSensor(QuboleSensor):
    __doc__ = '\n    Wait for a Hive partition to show up in QHS (Qubole Hive Service)\n    and check for its presence via QDS APIs\n\n    :param qubole_conn_id: Connection id which consists of qds auth_token\n    :type qubole_conn_id: str\n    :param data: a JSON object containing payload, whose presence needs to be checked.\n        Check this `example <https://github.com/apache/airflow/blob/master        /airflow/contrib/example_dags/example_qubole_sensor.py>`_ for sample payload\n        structure.\n    :type data: a JSON object\n\n    .. note:: Both ``data`` and ``qubole_conn_id`` fields support templating. You can\n        also use ``.txt`` files for template-driven use cases.\n    '

    @apply_defaults
    def __init__(self, *args, **kwargs):
        self.sensor_class = PartitionSensor
        (super(QubolePartitionSensor, self).__init__)(*args, **kwargs)