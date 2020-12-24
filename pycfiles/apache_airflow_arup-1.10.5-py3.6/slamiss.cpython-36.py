# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/slamiss.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1742 bytes
from sqlalchemy import Boolean, Column, String, Index, Text
from airflow.models.base import Base, ID_LEN
from airflow.utils.sqlalchemy import UtcDateTime

class SlaMiss(Base):
    __doc__ = '\n    Model that stores a history of the SLA that have been missed.\n    It is used to keep track of SLA failures over time and to avoid double\n    triggering alert emails.\n    '
    __tablename__ = 'sla_miss'
    task_id = Column((String(ID_LEN)), primary_key=True)
    dag_id = Column((String(ID_LEN)), primary_key=True)
    execution_date = Column(UtcDateTime, primary_key=True)
    email_sent = Column(Boolean, default=False)
    timestamp = Column(UtcDateTime)
    description = Column(Text)
    notification_sent = Column(Boolean, default=False)
    __table_args__ = (
     Index('sm_dag', dag_id, unique=False),)

    def __repr__(self):
        return str((
         self.dag_id, self.task_id, self.execution_date.isoformat()))