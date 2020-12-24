# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/openfaas_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3923 bytes
from airflow.hooks.base_hook import BaseHook
import requests
from airflow import AirflowException
OK_STATUS_CODE = 202

class OpenFaasHook(BaseHook):
    __doc__ = '\n    Interact with Openfaas to query, deploy, invoke and update function\n\n    :param function_name: Name of the function, Defaults to None\n    :type query: str\n    :param conn_id: openfass connection to use, Defaults to open_faas_default\n        for example host : http://openfaas.faas.com, Conn Type : Http\n    :type conn_id: str\n    '
    GET_FUNCTION = '/system/function/'
    INVOKE_ASYNC_FUNCTION = '/async-function/'
    DEPLOY_FUNCTION = '/system/functions'
    UPDATE_FUNCTION = '/system/functions'

    def __init__(self, function_name=None, conn_id='open_faas_default', *args, **kwargs):
        self.function_name = function_name
        self.conn_id = conn_id
        (super(BaseHook, self).__init__)(*args, **kwargs)

    def get_conn(self):
        conn = self.get_connection(self.conn_id)
        return conn

    def deploy_function(self, overwrite_function_if_exist, body):
        if overwrite_function_if_exist:
            self.log.info('Function already exist ' + self.function_name + ' going to update')
            self.update_function(body)
        else:
            url = self.get_conn().host + self.DEPLOY_FUNCTION
            self.log.info('Deploying function ' + url)
            response = requests.post(url, body)
            if response.status_code != OK_STATUS_CODE:
                self.log.error('Response status ' + str(response.status_code))
                self.log.error('Failed to deploy')
                raise AirflowException('failed to deploy')
            else:
                self.log.info('Function deployed ' + self.function_name)

    def invoke_async_function(self, body):
        url = self.get_conn().host + self.INVOKE_ASYNC_FUNCTION + self.function_name
        self.log.info('Invoking  function ' + url)
        response = requests.post(url, body)
        if response.ok:
            self.log.info('Invoked ' + self.function_name)
        else:
            self.log.error('Response status ' + str(response.status_code))
            raise AirflowException('failed to invoke function')

    def update_function(self, body):
        url = self.get_conn().host + self.UPDATE_FUNCTION
        self.log.info('Updating function ' + url)
        response = requests.put(url, body)
        if response.status_code != OK_STATUS_CODE:
            self.log.error('Response status ' + str(response.status_code))
            self.log.error('Failed to update response ' + response.content.decode('utf-8'))
            raise AirflowException('failed to update ' + self.function_name)
        else:
            self.log.info('Function was updated')

    def does_function_exist(self):
        url = self.get_conn().host + self.GET_FUNCTION + self.function_name
        response = requests.get(url)
        if response.ok:
            return True
        else:
            self.log.error('Failed to find function ' + self.function_name)
            return False