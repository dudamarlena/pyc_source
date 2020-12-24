# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/datadog_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3179 bytes
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.contrib.hooks.datadog_hook import DatadogHook
from airflow.utils import apply_defaults
from airflow.exceptions import AirflowException
from datadog import api

class DatadogSensor(BaseSensorOperator):
    """DatadogSensor"""
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