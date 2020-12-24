# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/sensors/jira_sensor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6131 bytes
from jira.resources import Resource
from airflow.contrib.operators.jira_operator import JIRAError
from airflow.contrib.operators.jira_operator import JiraOperator
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults

class JiraSensor(BaseSensorOperator):
    __doc__ = '\n    Monitors a jira ticket for any change.\n\n    :param jira_conn_id: reference to a pre-defined Jira Connection\n    :type jira_conn_id: str\n    :param method_name: method name from jira-python-sdk to be execute\n    :type method_name: str\n    :param method_params: parameters for the method method_name\n    :type method_params: dict\n    :param result_processor: function that return boolean and act as a sensor response\n    :type result_processor: function\n    '

    @apply_defaults
    def __init__(self, jira_conn_id='jira_default', method_name=None, method_params=None, result_processor=None, *args, **kwargs):
        (super(JiraSensor, self).__init__)(*args, **kwargs)
        self.jira_conn_id = jira_conn_id
        self.result_processor = None
        if result_processor is not None:
            self.result_processor = result_processor
        self.method_name = method_name
        self.method_params = method_params
        self.jira_operator = JiraOperator(task_id=(self.task_id), jira_conn_id=(self.jira_conn_id),
          jira_method=(self.method_name),
          jira_method_args=(self.method_params),
          result_processor=(self.result_processor))

    def poke(self, context):
        return self.jira_operator.execute(context=context)


class JiraTicketSensor(JiraSensor):
    __doc__ = '\n    Monitors a jira ticket for given change in terms of function.\n\n    :param jira_conn_id: reference to a pre-defined Jira Connection\n    :type jira_conn_id: str\n    :param ticket_id: id of the ticket to be monitored\n    :type ticket_id: str\n    :param field: field of the ticket to be monitored\n    :type field: str\n    :param expected_value: expected value of the field\n    :type expected_value: str\n    :param result_processor: function that return boolean and act as a sensor response\n    :type result_processor: function\n    '
    template_fields = ('ticket_id', )

    @apply_defaults
    def __init__(self, jira_conn_id='jira_default', ticket_id=None, field=None, expected_value=None, field_checker_func=None, *args, **kwargs):
        self.jira_conn_id = jira_conn_id
        self.ticket_id = ticket_id
        self.field = field
        self.expected_value = expected_value
        if field_checker_func is None:
            field_checker_func = self.issue_field_checker
        (super(JiraTicketSensor, self).__init__)(args, jira_conn_id=jira_conn_id, result_processor=field_checker_func, **kwargs)

    def poke(self, context):
        self.log.info('Jira Sensor checking for change in ticket: %s', self.ticket_id)
        self.jira_operator.method_name = 'issue'
        self.jira_operator.jira_method_args = {'id':self.ticket_id, 
         'fields':self.field}
        return JiraSensor.poke(self, context=context)

    def issue_field_checker(self, context, issue):
        result = None
        try:
            if issue is not None:
                if self.field is not None:
                    if self.expected_value is not None:
                        field_val = getattr(issue.fields, self.field)
                        if field_val is not None:
                            if isinstance(field_val, list):
                                result = self.expected_value in field_val
                            else:
                                if isinstance(field_val, str):
                                    result = self.expected_value.lower() == field_val.lower()
                                elif isinstance(field_val, Resource):
                                    if getattr(field_val, 'name'):
                                        result = self.expected_value.lower() == field_val.name.lower()
                                else:
                                    self.log.warning('Not implemented checker for issue field %s which is neither string nor list nor Jira Resource', self.field)
        except JIRAError as jira_error:
            self.log.error('Jira error while checking with expected value: %s', jira_error)
        except Exception as e:
            self.log.error('Error while checking with expected value %s:', self.expected_value)
            self.log.exception(e)

        if result is True:
            self.log.info('Issue field %s has expected value %s, returning success', self.field, self.expected_value)
        else:
            self.log.info("Issue field %s don't have expected value %s yet.", self.field, self.expected_value)
        return result