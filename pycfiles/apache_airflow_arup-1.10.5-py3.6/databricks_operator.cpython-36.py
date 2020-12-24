# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
    __doc__ = "\n    Submits a Spark job run to Databricks using the\n    `api/2.0/jobs/runs/submit\n    <https://docs.databricks.com/api/latest/jobs.html#runs-submit>`_\n    API endpoint.\n\n    There are two ways to instantiate this operator.\n\n    In the first way, you can take the JSON payload that you typically use\n    to call the ``api/2.0/jobs/runs/submit`` endpoint and pass it directly\n    to our ``DatabricksSubmitRunOperator`` through the ``json`` parameter.\n    For example ::\n\n        json = {\n          'new_cluster': {\n            'spark_version': '2.1.0-db3-scala2.11',\n            'num_workers': 2\n          },\n          'notebook_task': {\n            'notebook_path': '/Users/airflow@example.com/PrepareData',\n          },\n        }\n        notebook_run = DatabricksSubmitRunOperator(task_id='notebook_run', json=json)\n\n    Another way to accomplish the same thing is to use the named parameters\n    of the ``DatabricksSubmitRunOperator`` directly. Note that there is exactly\n    one named parameter for each top level parameter in the ``runs/submit``\n    endpoint. In this method, your code would look like this: ::\n\n        new_cluster = {\n          'spark_version': '2.1.0-db3-scala2.11',\n          'num_workers': 2\n        }\n        notebook_task = {\n          'notebook_path': '/Users/airflow@example.com/PrepareData',\n        }\n        notebook_run = DatabricksSubmitRunOperator(\n            task_id='notebook_run',\n            new_cluster=new_cluster,\n            notebook_task=notebook_task)\n\n    In the case where both the json parameter **AND** the named parameters\n    are provided, they will be merged together. If there are conflicts during the merge,\n    the named parameters will take precedence and override the top level ``json`` keys.\n\n    Currently the named parameters that ``DatabricksSubmitRunOperator`` supports are\n        - ``spark_jar_task``\n        - ``notebook_task``\n        - ``new_cluster``\n        - ``existing_cluster_id``\n        - ``libraries``\n        - ``run_name``\n        - ``timeout_seconds``\n\n    :param json: A JSON object containing API parameters which will be passed\n        directly to the ``api/2.0/jobs/runs/submit`` endpoint. The other named parameters\n        (i.e. ``spark_jar_task``, ``notebook_task``..) to this operator will\n        be merged with this json dictionary if they are provided.\n        If there are conflicts during the merge, the named parameters will\n        take precedence and override the top level json keys. (templated)\n\n        .. seealso::\n            For more information about templating see :ref:`jinja-templating`.\n            https://docs.databricks.com/api/latest/jobs.html#runs-submit\n    :type json: dict\n    :param spark_jar_task: The main class and parameters for the JAR task. Note that\n        the actual JAR is specified in the ``libraries``.\n        *EITHER* ``spark_jar_task`` *OR* ``notebook_task`` should be specified.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/jobs.html#jobssparkjartask\n    :type spark_jar_task: dict\n    :param notebook_task: The notebook path and parameters for the notebook task.\n        *EITHER* ``spark_jar_task`` *OR* ``notebook_task`` should be specified.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/jobs.html#jobsnotebooktask\n    :type notebook_task: dict\n    :param new_cluster: Specs for a new cluster on which this task will be run.\n        *EITHER* ``new_cluster`` *OR* ``existing_cluster_id`` should be specified.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/jobs.html#jobsclusterspecnewcluster\n    :type new_cluster: dict\n    :param existing_cluster_id: ID for existing cluster on which to run this task.\n        *EITHER* ``new_cluster`` *OR* ``existing_cluster_id`` should be specified.\n        This field will be templated.\n    :type existing_cluster_id: str\n    :param libraries: Libraries which this run will use.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/libraries.html#managedlibrarieslibrary\n    :type libraries: list of dicts\n    :param run_name: The run name used for this task.\n        By default this will be set to the Airflow ``task_id``. This ``task_id`` is a\n        required parameter of the superclass ``BaseOperator``.\n        This field will be templated.\n    :type run_name: str\n    :param timeout_seconds: The timeout for this run. By default a value of 0 is used\n        which means to have no timeout.\n        This field will be templated.\n    :type timeout_seconds: int32\n    :param databricks_conn_id: The name of the Airflow connection to use.\n        By default and in the common case this will be ``databricks_default``. To use\n        token based authentication, provide the key ``token`` in the extra field for the\n        connection.\n    :type databricks_conn_id: str\n    :param polling_period_seconds: Controls the rate which we poll for the result of\n        this run. By default the operator will poll every 30 seconds.\n    :type polling_period_seconds: int\n    :param databricks_retry_limit: Amount of times retry if the Databricks backend is\n        unreachable. Its value must be greater than or equal to 1.\n    :type databricks_retry_limit: int\n    :param databricks_retry_delay: Number of seconds to wait between retries (it\n            might be a floating point number).\n    :type databricks_retry_delay: float\n    :param do_xcom_push: Whether we should push run_id and run_page_url to xcom.\n    :type do_xcom_push: bool\n    "
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
    __doc__ = '\n    Runs an existing Spark job run to Databricks using the\n    `api/2.0/jobs/run-now\n    <https://docs.databricks.com/api/latest/jobs.html#run-now>`_\n    API endpoint.\n\n    There are two ways to instantiate this operator.\n\n    In the first way, you can take the JSON payload that you typically use\n    to call the ``api/2.0/jobs/run-now`` endpoint and pass it directly\n    to our ``DatabricksRunNowOperator`` through the ``json`` parameter.\n    For example ::\n\n        json = {\n          "job_id": 42,\n          "notebook_params": {\n            "dry-run": "true",\n            "oldest-time-to-consider": "1457570074236"\n          }\n        }\n\n        notebook_run = DatabricksRunNowOperator(task_id=\'notebook_run\', json=json)\n\n    Another way to accomplish the same thing is to use the named parameters\n    of the ``DatabricksRunNowOperator`` directly. Note that there is exactly\n    one named parameter for each top level parameter in the ``run-now``\n    endpoint. In this method, your code would look like this: ::\n\n        job_id=42\n\n        notebook_params = {\n            "dry-run": "true",\n            "oldest-time-to-consider": "1457570074236"\n        }\n\n        python_params = ["douglas adams", "42"]\n\n        spark_submit_params = ["--class", "org.apache.spark.examples.SparkPi"]\n\n        notebook_run = DatabricksRunNowOperator(\n            job_id=job_id,\n            notebook_params=notebook_params,\n            python_params=python_params,\n            spark_submit_params=spark_submit_params\n        )\n\n    In the case where both the json parameter **AND** the named parameters\n    are provided, they will be merged together. If there are conflicts during the merge,\n    the named parameters will take precedence and override the top level ``json`` keys.\n\n    Currently the named parameters that ``DatabricksRunNowOperator`` supports are\n        - ``job_id``\n        - ``json``\n        - ``notebook_params``\n        - ``python_params``\n        - ``spark_submit_params``\n\n\n    :param job_id: the job_id of the existing Databricks job.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/jobs.html#run-now\n    :type job_id: str\n    :param json: A JSON object containing API parameters which will be passed\n        directly to the ``api/2.0/jobs/run-now`` endpoint. The other named parameters\n        (i.e. ``notebook_params``, ``spark_submit_params``..) to this operator will\n        be merged with this json dictionary if they are provided.\n        If there are conflicts during the merge, the named parameters will\n        take precedence and override the top level json keys. (templated)\n\n        .. seealso::\n            For more information about templating see :ref:`jinja-templating`.\n            https://docs.databricks.com/api/latest/jobs.html#run-now\n    :type json: dict\n    :param notebook_params: A dict from keys to values for jobs with notebook task,\n        e.g. "notebook_params": {"name": "john doe", "age":  "35"}.\n        The map is passed to the notebook and will be accessible through the\n        dbutils.widgets.get function. See Widgets for more information.\n        If not specified upon run-now, the triggered run will use the\n        job’s base parameters. notebook_params cannot be\n        specified in conjunction with jar_params. The json representation\n        of this field (i.e. {"notebook_params":{"name":"john doe","age":"35"}})\n        cannot exceed 10,000 bytes.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/user-guide/notebooks/widgets.html\n    :type notebook_params: dict\n    :param python_params: A list of parameters for jobs with python tasks,\n        e.g. "python_params": ["john doe", "35"].\n        The parameters will be passed to python file as command line parameters.\n        If specified upon run-now, it would overwrite the parameters specified in\n        job setting.\n        The json representation of this field (i.e. {"python_params":["john doe","35"]})\n        cannot exceed 10,000 bytes.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/jobs.html#run-now\n    :type python_params: list[str]\n    :param spark_submit_params: A list of parameters for jobs with spark submit task,\n        e.g. "spark_submit_params": ["--class", "org.apache.spark.examples.SparkPi"].\n        The parameters will be passed to spark-submit script as command line parameters.\n        If specified upon run-now, it would overwrite the parameters specified\n        in job setting.\n        The json representation of this field cannot exceed 10,000 bytes.\n        This field will be templated.\n\n        .. seealso::\n            https://docs.databricks.com/api/latest/jobs.html#run-now\n    :type spark_submit_params: list[str]\n    :param timeout_seconds: The timeout for this run. By default a value of 0 is used\n        which means to have no timeout.\n        This field will be templated.\n    :type timeout_seconds: int32\n    :param databricks_conn_id: The name of the Airflow connection to use.\n        By default and in the common case this will be ``databricks_default``. To use\n        token based authentication, provide the key ``token`` in the extra field for the\n        connection.\n    :type databricks_conn_id: str\n    :param polling_period_seconds: Controls the rate which we poll for the result of\n        this run. By default the operator will poll every 30 seconds.\n    :type polling_period_seconds: int\n    :param databricks_retry_limit: Amount of times retry if the Databricks backend is\n        unreachable. Its value must be greater than or equal to 1.\n    :type databricks_retry_limit: int\n    :param do_xcom_push: Whether we should push run_id and run_page_url to xcom.\n    :type do_xcom_push: bool\n    '
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