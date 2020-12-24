# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/log.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 2230 bytes
from sqlalchemy import Column, Integer, String, Text, Index
from airflow.models.base import Base, ID_LEN
from airflow.utils import timezone
from airflow.utils.sqlalchemy import UtcDateTime

class Log(Base):
    __doc__ = '\n    Used to actively log events to the database\n    '
    __tablename__ = 'log'
    id = Column(Integer, primary_key=True)
    dttm = Column(UtcDateTime)
    dag_id = Column(String(ID_LEN))
    task_id = Column(String(ID_LEN))
    event = Column(String(30))
    execution_date = Column(UtcDateTime)
    owner = Column(String(500))
    extra = Column(Text)
    __table_args__ = (
     Index('idx_log_dag', dag_id),)

    def __init__(self, event, task_instance, owner=None, extra=None, **kwargs):
        self.dttm = timezone.utcnow()
        self.event = event
        self.extra = extra
        task_owner = None
        if task_instance:
            self.dag_id = task_instance.dag_id
            self.task_id = task_instance.task_id
            self.execution_date = task_instance.execution_date
            task_owner = task_instance.task.owner
        if 'task_id' in kwargs:
            self.task_id = kwargs['task_id']
        if 'dag_id' in kwargs:
            self.dag_id = kwargs['dag_id']
        if 'execution_date' in kwargs:
            if kwargs['execution_date']:
                self.execution_date = kwargs['execution_date']
        self.owner = owner or task_owner