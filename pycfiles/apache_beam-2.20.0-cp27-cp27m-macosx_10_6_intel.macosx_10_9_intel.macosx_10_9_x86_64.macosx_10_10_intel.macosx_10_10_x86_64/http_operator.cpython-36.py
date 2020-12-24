# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/http_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4015 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SimpleHttpOperator(BaseOperator):
    """SimpleHttpOperator"""
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