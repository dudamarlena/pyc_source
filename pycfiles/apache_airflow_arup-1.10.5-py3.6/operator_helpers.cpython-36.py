# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/operator_helpers.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 3018 bytes
AIRFLOW_VAR_NAME_FORMAT_MAPPING = {'AIRFLOW_CONTEXT_DAG_ID':{'default':'airflow.ctx.dag_id', 
  'env_var_format':'AIRFLOW_CTX_DAG_ID'}, 
 'AIRFLOW_CONTEXT_TASK_ID':{'default':'airflow.ctx.task_id', 
  'env_var_format':'AIRFLOW_CTX_TASK_ID'}, 
 'AIRFLOW_CONTEXT_EXECUTION_DATE':{'default':'airflow.ctx.execution_date', 
  'env_var_format':'AIRFLOW_CTX_EXECUTION_DATE'}, 
 'AIRFLOW_CONTEXT_DAG_RUN_ID':{'default':'airflow.ctx.dag_run_id', 
  'env_var_format':'AIRFLOW_CTX_DAG_RUN_ID'}}

def context_to_airflow_vars(context, in_env_var_format=False):
    """
    Given a context, this function provides a dictionary of values that can be used to
    externally reconstruct relations between dags, dag_runs, tasks and task_instances.
    Default to abc.def.ghi format and can be made to ABC_DEF_GHI format if
    in_env_var_format is set to True.

    :param context: The context for the task_instance of interest.
    :type context: dict
    :param in_env_var_format: If returned vars should be in ABC_DEF_GHI format.
    :type in_env_var_format: bool
    :return: task_instance context as dict.
    """
    params = dict()
    if in_env_var_format:
        name_format = 'env_var_format'
    else:
        name_format = 'default'
    task_instance = context.get('task_instance')
    if task_instance:
        if task_instance.dag_id:
            params[AIRFLOW_VAR_NAME_FORMAT_MAPPING['AIRFLOW_CONTEXT_DAG_ID'][name_format]] = task_instance.dag_id
    if task_instance:
        if task_instance.task_id:
            params[AIRFLOW_VAR_NAME_FORMAT_MAPPING['AIRFLOW_CONTEXT_TASK_ID'][name_format]] = task_instance.task_id
    if task_instance:
        if task_instance.execution_date:
            params[AIRFLOW_VAR_NAME_FORMAT_MAPPING['AIRFLOW_CONTEXT_EXECUTION_DATE'][name_format]] = task_instance.execution_date.isoformat()
    dag_run = context.get('dag_run')
    if dag_run:
        if dag_run.run_id:
            params[AIRFLOW_VAR_NAME_FORMAT_MAPPING['AIRFLOW_CONTEXT_DAG_RUN_ID'][name_format]] = dag_run.run_id
    return params