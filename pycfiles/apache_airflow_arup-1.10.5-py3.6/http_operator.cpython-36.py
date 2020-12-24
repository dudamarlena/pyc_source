# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/http_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4015 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SimpleHttpOperator(BaseOperator):
    __doc__ = '\n    Calls an endpoint on an HTTP system to execute an action\n\n    :param http_conn_id: The connection to run the operator against\n    :type http_conn_id: str\n    :param endpoint: The relative part of the full url. (templated)\n    :type endpoint: str\n    :param method: The HTTP method to use, default = "POST"\n    :type method: str\n    :param data: The data to pass. POST-data in POST/PUT and params\n        in the URL for a GET request. (templated)\n    :type data: For POST/PUT, depends on the content-type parameter,\n        for GET a dictionary of key/value string pairs\n    :param headers: The HTTP headers to be added to the GET request\n    :type headers: a dictionary of string key/value pairs\n    :param response_check: A check against the \'requests\' response object.\n        Returns True for \'pass\' and False otherwise.\n    :type response_check: A lambda or defined function.\n    :param extra_options: Extra options for the \'requests\' library, see the\n        \'requests\' documentation (options to modify timeout, ssl, etc.)\n    :type extra_options: A dictionary of options, where key is string and value\n        depends on the option that\'s being modified.\n    :param xcom_push: Push the response to Xcom (default: False).\n        If xcom_push is True, response of an HTTP request will also\n        be pushed to an XCom.\n    :type xcom_push: bool\n    :param log_response: Log the response (default: False)\n    :type log_response: bool\n    '
    template_fields = [
     'endpoint', 'data', 'headers']
    template_ext = ()
    ui_color = '#f4a460'

    @apply_defaults
    def __init__(self, endpoint, method='POST', data=None, headers=None, response_check=None, extra_options=None, xcom_push=False, http_conn_id='http_default', log_response=False, *args, **kwargs):
        (super(SimpleHttpOperator, self).__init__)(*args, **kwargs)
        self.http_conn_id = http_conn_id
        self.method = method
        self.endpoint = endpoint
        self.headers = headers or {}
        self.data = data or {}
        self.response_check = response_check
        self.extra_options = extra_options or {}
        self.xcom_push_flag = xcom_push
        self.log_response = log_response

    def execute(self, context):
        http = HttpHook((self.method), http_conn_id=(self.http_conn_id))
        self.log.info('Calling HTTP method')
        response = http.run(self.endpoint, self.data, self.headers, self.extra_options)
        if self.log_response:
            self.log.info(response.text)
        if self.response_check:
            if not self.response_check(response):
                raise AirflowException('Response check returned False.')
        if self.xcom_push_flag:
            return response.text