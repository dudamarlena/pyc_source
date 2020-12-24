# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/api/common/experimental/delete_dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2617 bytes
"""Delete DAGs APIs."""
import os
from sqlalchemy import or_
from airflow import models
from airflow.models import TaskFail, DagModel
from airflow.utils.db import provide_session
from airflow.exceptions import DagFileExists, DagNotFound

@provide_session
def delete_dag(dag_id, keep_records_in_log=True, session=None):
    """
    :param dag_id: the dag_id of the DAG to delete
    :param keep_records_in_log: whether keep records of the given dag_id
        in the Log table in the backend database (for reasons like auditing).
        The default value is True.
    :param session: session used
    :return count of deleted dags
    """
    dag = session.query(DagModel).filter(DagModel.dag_id == dag_id).first()
    if dag is None:
        raise DagNotFound('Dag id {} not found'.format(dag_id))
    if dag.fileloc:
        if os.path.exists(dag.fileloc):
            raise DagFileExists('Dag id {} is still in DagBag. Remove the DAG file first: {}'.format(dag_id, dag.fileloc))
    count = 0
    for model in models.base.Base._decl_class_registry.values():
        if hasattr(model, 'dag_id'):
            if keep_records_in_log:
                if model.__name__ == 'Log':
                    continue
            cond = or_(model.dag_id == dag_id, model.dag_id.like(dag_id + '.%'))
            count += session.query(model).filter(cond).delete(synchronize_session='fetch')

    if dag.is_subdag:
        parent_dag_id, task_id = dag_id.rsplit('.', 1)
        for model in (models.DagRun, TaskFail, models.TaskInstance):
            count += session.query(model).filter(model.dag_id == parent_dag_id, model.task_id == task_id).delete()

    return count