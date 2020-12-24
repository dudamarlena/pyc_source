# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/taskreschedule.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 3319 bytes
from sqlalchemy import Column, ForeignKeyConstraint, Index, Integer, String, asc
from airflow.models.base import Base, ID_LEN
from airflow.utils.db import provide_session
from airflow.utils.sqlalchemy import UtcDateTime

class TaskReschedule(Base):
    __doc__ = '\n    TaskReschedule tracks rescheduled task instances.\n    '
    __tablename__ = 'task_reschedule'
    id = Column(Integer, primary_key=True)
    task_id = Column((String(ID_LEN)), nullable=False)
    dag_id = Column((String(ID_LEN)), nullable=False)
    execution_date = Column(UtcDateTime, nullable=False)
    try_number = Column(Integer, nullable=False)
    start_date = Column(UtcDateTime, nullable=False)
    end_date = Column(UtcDateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    reschedule_date = Column(UtcDateTime, nullable=False)
    __table_args__ = (
     Index('idx_task_reschedule_dag_task_date', dag_id, task_id, execution_date, unique=False),
     ForeignKeyConstraint([task_id, dag_id, execution_date], [
      'task_instance.task_id', 'task_instance.dag_id',
      'task_instance.execution_date'],
       name='task_reschedule_dag_task_date_fkey',
       ondelete='CASCADE'))

    def __init__(self, task, execution_date, try_number, start_date, end_date, reschedule_date):
        self.dag_id = task.dag_id
        self.task_id = task.task_id
        self.execution_date = execution_date
        self.try_number = try_number
        self.start_date = start_date
        self.end_date = end_date
        self.reschedule_date = reschedule_date
        self.duration = (self.end_date - self.start_date).total_seconds()

    @staticmethod
    @provide_session
    def find_for_task_instance(task_instance, session):
        """
        Returns all task reschedules for the task instance and try number,
        in ascending order.

        :param task_instance: the task instance to find task reschedules for
        :type task_instance: airflow.models.TaskInstance
        """
        TR = TaskReschedule
        return session.query(TR).filter(TR.dag_id == task_instance.dag_id, TR.task_id == task_instance.task_id, TR.execution_date == task_instance.execution_date, TR.try_number == task_instance.try_number).order_by(asc(TR.id)).all()