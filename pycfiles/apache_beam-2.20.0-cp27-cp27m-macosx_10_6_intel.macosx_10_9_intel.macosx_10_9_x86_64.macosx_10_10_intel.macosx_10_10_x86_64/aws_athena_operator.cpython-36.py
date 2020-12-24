# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/aws_athena_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5183 bytes
from uuid import uuid4
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.contrib.hooks.aws_athena_hook import AWSAthenaHook

class AWSAthenaOperator(BaseOperator):
    """AWSAthenaOperator"""
    ui_color = '#44b5e2'
    template_fields = ('query', 'database', 'output_location')
    template_ext = ('.sql', )

    @apply_defaults
    def __init__(self, query, database, output_location, aws_conn_id='aws_default', client_request_token=None, query_execution_context=None, result_configuration=None, sleep_time=30, max_tries=None, *args, **kwargs):
        (super(AWSAthenaOperator, self).__init__)(*args, **kwargs)
        self.query = query
        self.database = database
        self.output_location = output_location
        self.aws_conn_id = aws_conn_id
        self.client_request_token = client_request_token or str(uuid4())
        self.query_execution_context = query_execution_context or {}
        self.result_configuration = result_configuration or {}
        self.sleep_time = sleep_time
        self.max_tries = max_tries
        self.query_execution_id = None
        self.hook = None

    def get_hook(self):
        return AWSAthenaHook(self.aws_conn_id, self.sleep_time)

    def execute(self, context):
        """
        Run Presto Query on Athena
        """
        self.hook = self.get_hook()
        self.query_execution_context['Database'] = self.database
        self.result_configuration['OutputLocation'] = self.output_location
        self.query_execution_id = self.hook.run_query(self.query, self.query_execution_context, self.result_configuration, self.client_request_token)
        query_status = self.hook.poll_query_status(self.query_execution_id, self.max_tries)
        if query_status in AWSAthenaHook.FAILURE_STATES:
            error_message = self.hook.get_state_change_reason(self.query_execution_id)
            raise Exception('Final state of Athena job is {}, query_execution_id is {}. Error: {}'.format(query_status, self.query_execution_id, error_message))
        else:
            if not query_status or query_status in AWSAthenaHook.INTERMEDIATE_STATES:
                raise Exception('Final state of Athena job is {}. Max tries of poll status exceeded, query_execution_id is {}.'.format(query_status, self.query_execution_id))
        return self.query_execution_id

    def on_kill(self):
        """
        Cancel the submitted athena query
        """
        if self.query_execution_id:
            self.log.info('⚰️⚰️⚰️ Received a kill Signal. Time to Die')
            self.log.info('Stopping Query with executionId - %s', self.query_execution_id)
            response = self.hook.stop_query(self.query_execution_id)
            http_status_code = None
            try:
                try:
                    http_status_code = response['ResponseMetadata']['HTTPStatusCode']
                except Exception as ex:
                    self.log.error('Exception while cancelling query', ex)

            finally:
                if http_status_code is None or http_status_code != 200:
                    self.log.error('Unable to request query cancel on athena. Exiting')
                else:
                    self.log.info('Polling Athena for query with id %s to reach final state', self.query_execution_id)
                    self.hook.poll_query_status(self.query_execution_id)