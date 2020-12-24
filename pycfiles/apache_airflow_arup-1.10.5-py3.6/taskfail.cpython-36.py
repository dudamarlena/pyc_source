# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/taskfail.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1978 bytes
from sqlalchemy import Column, Index, Integer, String
from airflow.models.base import Base, ID_LEN
from airflow.utils.sqlalchemy import UtcDateTime

class TaskFail(Base):
    __doc__ = '\n    TaskFail tracks the failed run durations of each task instance.\n    '
    __tablename__ = 'task_fail'
    id = Column(Integer, primary_key=True)
    task_id = Column((String(ID_LEN)), nullable=False)
    dag_id = Column((String(ID_LEN)), nullable=False)
    execution_date = Column(UtcDateTime, nullable=False)
    start_date = Column(UtcDateTime)
    end_date = Column(UtcDateTime)
    duration = Column(Integer)
    __table_args__ = (
     Index('idx_task_fail_dag_task_date', dag_id, task_id, execution_date, unique=False),)

    def __init__(self, task, execution_date, start_date, end_date):
        self.dag_id = task.dag_id
        self.task_id = task.task_id
        self.execution_date = execution_date
        self.start_date = start_date
        self.end_date = end_date
        if self.end_date:
            if self.start_date:
                self.duration = int((self.end_date - self.start_date).total_seconds())
        else:
            self.duration = None