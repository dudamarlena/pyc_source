# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/databricks_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 20294 bytes
import six, time
from airflow.exceptions import AirflowException
from airflow.contrib.hooks.databricks_hook import DatabricksHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
XCOM_RUN_ID_KEY = 'run_id'
XCOM_RUN_PAGE_URL_KEY = 'run_page_url'

def _deep_string_coerce(content, json_path='json'):
    """
    Coerces content or all values of content if it is a dict to a string. The
    function will throw if content contains non-string or non-numeric types.

    The reason why we have this function is because the ``self.json`` field must be a
    dict with only string values. This is because ``render_template`` will fail
    for numerical values.
    """
    c = _deep_string_coerce
    if isinstance(content, six.string_types):
        return content
    if isinstance(content, six.integer_types + (float,)):
        return str(content)
    if isinstance(content, (list, tuple)):
        return [c(e, '{0}[{1}]'.format(json_path, i)) for i, e in enumerate(content)]
    if isinstance(content, dict):
        return {k:c(v, '{0}[{1}]'.format(json_path, k)) for k, v in list(content.items())}
    param_type = type(content)
    msg = 'Type {0} used for parameter {1} is not a number or a string'.format(param_type, json_path)
    raise AirflowException(msg)


def _handle_databricks_operator_execution(operator, hook, log, context):
    """
    Handles the Airflow + Databricks lifecycle logic for a Databricks operator

    :param operator: Databricks operator being handled
    :param context: Airflow context
    """
    if operator.do_xcom_push:
        context['ti'].xcom_push(key=XCOM_RUN_ID_KEY, value=(operator.run_id))
    log.info('Run submitted with run_id: %s', operator.run_id)
    run_page_url = hook.get_run_page_url(operator.run_id)
    if operator.do_xcom_push:
        context['ti'].xcom_push(key=XCOM_RUN_PAGE_URL_KEY, value=run_page_url)
    log.info('View run status, Spark UI, and logs at %s', run_page_url)
    while True:
        run_state = hook.get_run_state(operator.run_id)
        if run_state.is_terminal:
            if run_state.is_successful:
                log.info('%s completed successfully.', operator.task_id)
                log.info('View run status, Spark UI, and logs at %s', run_page_url)
                return
            error_message = '{t} failed with terminal state: {s}'.format(t=(operator.task_id),
              s=run_state)
            raise AirflowException(error_message)
        else:
            log.info('%s in run state: %s', operator.task_id, run_state)
            log.info('View run status, Spark UI, and logs at %s', run_page_url)
            log.info('Sleeping for %s seconds.', operator.polling_period_seconds)
            time.sleep(operator.polling_period_seconds)


class DatabricksSubmitRunOperator(BaseOperator):
    """DatabricksSubmitRunOperator"""
    template_fields = ('json', )
    ui_color = '#1CB1C2'
    ui_fgcolor = '#fff'

    @apply_defaults
    def __init__(self, json=None, spark_jar_task=None, notebook_task=None, new_cluster=None, existing_cluster_id=None, libraries=None, run_name=None, timeout_seconds=None, databricks_conn_id='databricks_default', polling_period_seconds=30, databricks_retry_limit=3, databricks_retry_delay=1, do_xcom_push=False, **kwargs):
        """
        Creates a new ``DatabricksSubmitRunOperator``.
        """
        (super(DatabricksSubmitRunOperator, self).__init__)(**kwargs)
        self.json = json or {}
        self.databricks_conn_id = databricks_conn_id
        self.polling_period_seconds = polling_period_seconds
        self.databricks_retry_limit = databricks_retry_limit
        self.databricks_retry_delay = databricks_retry_delay
        if spark_jar_task is not None:
            self.json['spark_jar_task'] = spark_jar_task
        if notebook_task is not None:
            self.json['notebook_task'] = notebook_task
        if new_cluster is not None:
            self.json['new_cluster'] = new_cluster
        if existing_cluster_id is not None:
            self.json['existing_cluster_id'] = existing_cluster_id
        if libraries is not None:
            self.json['libraries'] = libraries
        if run_name is not None:
            self.json['run_name'] = run_name
        if timeout_seconds is not None:
            self.json['timeout_seconds'] = timeout_seconds
        if 'run_name' not in self.json:
            self.json['run_name'] = run_name or kwargs['task_id']
        self.json = _deep_string_coerce(self.json)
        self.run_id = None
        self.do_xcom_push = do_xcom_push

    def get_hook(self):
        return DatabricksHook((self.databricks_conn_id),
          retry_limit=(self.databricks_retry_limit),
          retry_delay=(self.databricks_retry_delay))

    def execute(self, context):
        hook = self.get_hook()
        self.run_id = hook.submit_run(self.json)
        _handle_databricks_operator_execution(self, hook, self.log, context)

    def on_kill(self):
        hook = self.get_hook()
        hook.cancel_run(self.run_id)
        self.log.info('Task: %s with run_id: %s was requested to be cancelled.', self.task_id, self.run_id)


class DatabricksRunNowOperator(BaseOperator):
    """DatabricksRunNowOperator"""
    template_fields = ('json', )
    ui_color = '#1CB1C2'
    ui_fgcolor = '#fff'

    @apply_defaults
    def __init__(self, job_id, json=None, notebook_params=None, python_params=None, spark_submit_params=None, databricks_conn_id='databricks_default', polling_period_seconds=30, databricks_retry_limit=3, databricks_retry_delay=1, do_xcom_push=False, **kwargs):
        """
        Creates a new ``DatabricksRunNowOperator``.
        """
        (super(DatabricksRunNowOperator, self).__init__)(**kwargs)
        self.json = json or {}
        self.databricks_conn_id = databricks_conn_id
        self.polling_period_seconds = polling_period_seconds
        self.databricks_retry_limit = databricks_retry_limit
        self.databricks_retry_delay = databricks_retry_delay
        if job_id is not None:
            self.json['job_id'] = job_id
        if notebook_params is not None:
            self.json['notebook_params'] = notebook_params
        if python_params is not None:
            self.json['python_params'] = python_params
        if spark_submit_params is not None:
            self.json['spark_submit_params'] = spark_submit_params
        self.json = _deep_string_coerce(self.json)
        self.run_id = None
        self.do_xcom_push = do_xcom_push

    def get_hook(self):
        return DatabricksHook((self.databricks_conn_id),
          retry_limit=(self.databricks_retry_limit),
          retry_delay=(self.databricks_retry_delay))

    def execute(self, context):
        hook = self.get_hook()
        self.run_id = hook.run_now(self.json)
        _handle_databricks_operator_execution(self, hook, self.log, context)

    def on_kill(self):
        hook = self.get_hook()
        hook.cancel_run(self.run_id)
        self.log.info('Task: %s with run_id: %s was requested to be cancelled.', self.task_id, self.run_id)