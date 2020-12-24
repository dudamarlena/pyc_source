# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/sensors/http_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3611 bytes
from builtins import str
from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class HttpSensor(BaseSensorOperator):
    __doc__ = "\n    Executes a HTTP get statement and returns False on failure:\n        404 not found or response_check function returned False\n\n    :param http_conn_id: The connection to run the sensor against\n    :type http_conn_id: str\n    :param method: The HTTP request method to use\n    :type method: str\n    :param endpoint: The relative part of the full url\n    :type endpoint: str\n    :param request_params: The parameters to be added to the GET url\n    :type request_params: a dictionary of string key/value pairs\n    :param headers: The HTTP headers to be added to the GET request\n    :type headers: a dictionary of string key/value pairs\n    :param response_check: A check against the 'requests' response object.\n        Returns True for 'pass' and False otherwise.\n    :type response_check: A lambda or defined function.\n    :param extra_options: Extra options for the 'requests' library, see the\n        'requests' documentation (options to modify timeout, ssl, etc.)\n    :type extra_options: A dictionary of options, where key is string and value\n        depends on the option that's being modified.\n    "
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