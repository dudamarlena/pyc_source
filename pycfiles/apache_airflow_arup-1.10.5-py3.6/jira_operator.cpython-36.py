# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/jira_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4290 bytes
from airflow.contrib.hooks.jira_hook import JIRAError
from airflow.contrib.hooks.jira_hook import JiraHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class JiraOperator(BaseOperator):
    __doc__ = '\n    JiraOperator to interact and perform action on Jira issue tracking system.\n    This operator is designed to use Jira Python SDK: http://jira.readthedocs.io\n\n    :param jira_conn_id: reference to a pre-defined Jira Connection\n    :type jira_conn_id: str\n    :param jira_method: method name from Jira Python SDK to be called\n    :type jira_method: str\n    :param jira_method_args: required method parameters for the jira_method. (templated)\n    :type jira_method_args: dict\n    :param result_processor: function to further process the response from Jira\n    :type result_processor: function\n    :param get_jira_resource_method: function or operator to get jira resource\n                                    on which the provided jira_method will be executed\n    :type get_jira_resource_method: function\n    '
    template_fields = ('jira_method_args', )

    @apply_defaults
    def __init__(self, jira_conn_id='jira_default', jira_method=None, jira_method_args=None, result_processor=None, get_jira_resource_method=None, *args, **kwargs):
        (super(JiraOperator, self).__init__)(*args, **kwargs)
        self.jira_conn_id = jira_conn_id
        self.method_name = jira_method
        self.jira_method_args = jira_method_args
        self.result_processor = result_processor
        self.get_jira_resource_method = get_jira_resource_method

    def execute(self, context):
        try:
            if self.get_jira_resource_method is not None:
                if isinstance(self.get_jira_resource_method, JiraOperator):
                    resource = (self.get_jira_resource_method.execute)(**context)
                else:
                    resource = (self.get_jira_resource_method)(**context)
            else:
                hook = JiraHook(jira_conn_id=(self.jira_conn_id))
                resource = hook.client
            jira_result = (getattr(resource, self.method_name))(**self.jira_method_args)
            if self.result_processor:
                return self.result_processor(context, jira_result)
            return jira_result
        except JIRAError as jira_error:
            raise AirflowException('Failed to execute jiraOperator, error: %s' % str(jira_error))
        except Exception as e:
            raise AirflowException('Jira operator error: %s' % str(e))