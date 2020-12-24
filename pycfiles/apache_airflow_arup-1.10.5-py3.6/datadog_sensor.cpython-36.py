# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/datadog_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3179 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.contrib.hooks.datadog_hook import DatadogHook
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException
from datadog import api

class DatadogSensor(BaseSensorOperator):
    __doc__ = '\n    A sensor to listen, with a filter, to datadog event streams and determine\n    if some event was emitted.\n\n    Depends on the datadog API, which has to be deployed on the same server where\n    Airflow runs.\n\n    :param datadog_conn_id: The connection to datadog, containing metadata for api keys.\n    :param datadog_conn_id: str\n    '
    ui_color = '#66c3dd'

    @apply_defaults
    def __init__(self, datadog_conn_id='datadog_default', from_seconds_ago=3600, up_to_seconds_from_now=0, priority=None, sources=None, tags=None, response_check=None, *args, **kwargs):
        (super(DatadogSensor, self).__init__)(*args, **kwargs)
        self.datadog_conn_id = datadog_conn_id
        self.from_seconds_ago = from_seconds_ago
        self.up_to_seconds_from_now = up_to_seconds_from_now
        self.priority = priority
        self.sources = sources
        self.tags = tags
        self.response_check = response_check

    def poke(self, context):
        DatadogHook(datadog_conn_id=(self.datadog_conn_id))
        response = api.Event.query(start=(self.from_seconds_ago),
          end=(self.up_to_seconds_from_now),
          priority=(self.priority),
          sources=(self.sources),
          tags=(self.tags))
        if isinstance(response, dict):
            if response.get('status', 'ok') != 'ok':
                self.log.error('Unexpected Datadog result: %s', response)
                raise AirflowException('Datadog returned unexpected result')
        if self.response_check:
            return self.response_check(response)
        else:
            return len(response) > 0