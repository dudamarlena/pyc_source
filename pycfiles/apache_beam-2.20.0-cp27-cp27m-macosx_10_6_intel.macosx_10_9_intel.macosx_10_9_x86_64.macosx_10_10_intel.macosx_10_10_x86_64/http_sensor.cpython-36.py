# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/http_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3611 bytes
from builtins import str
from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class HttpSensor(BaseSensorOperator):
    """HttpSensor"""
    template_fields = ('endpoint', 'request_params')

    @apply_defaults
    def __init__(self, endpoint, http_conn_id='http_default', method='GET', request_params=None, headers=None, response_check=None, extra_options=None, *args, **kwargs):
        (super(HttpSensor, self).__init__)(*args, **kwargs)
        self.endpoint = endpoint
        self.http_conn_id = http_conn_id
        self.request_params = request_params or {}
        self.headers = headers or {}
        self.extra_options = extra_options or {}
        self.response_check = response_check
        self.hook = HttpHook(method=method,
          http_conn_id=http_conn_id)

    def poke(self, context):
        self.log.info('Poking: %s', self.endpoint)
        try:
            response = self.hook.run((self.endpoint), data=(self.request_params),
              headers=(self.headers),
              extra_options=(self.extra_options))
            if self.response_check:
                return self.response_check(response)
        except AirflowException as ae:
            if str(ae).startswith('404'):
                return False
            raise ae

        return True