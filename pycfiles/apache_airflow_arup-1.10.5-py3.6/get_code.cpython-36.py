# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/common/experimental/get_code.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1487 bytes
"""Get code APIs."""
from airflow.api.common.experimental import check_and_get_dag
from airflow.exceptions import AirflowException
from airflow.www import utils as wwwutils

def get_code(dag_id):
    """Return python code of a given dag_id.

    :param dag_id: DAG id
    :return: code of the DAG
    """
    dag = check_and_get_dag(dag_id=dag_id)
    try:
        with wwwutils.open_maybe_zipped(dag.fileloc, 'r') as (file):
            code = file.read()
            return code
    except IOError as exception:
        error_message = 'Error {} while reading Dag id {} Code'.format(str(exception), dag_id)
        raise AirflowException(error_message)