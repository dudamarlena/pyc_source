# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/dagpickle.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1940 bytes
import dill
from sqlalchemy import Column, Integer, PickleType, Text
from airflow.models.base import Base
from airflow.utils import timezone
from airflow.utils.sqlalchemy import UtcDateTime

class DagPickle(Base):
    """DagPickle"""
    id = Column(Integer, primary_key=True)
    pickle = Column(PickleType(pickler=dill))
    created_dttm = Column(UtcDateTime, default=(timezone.utcnow))
    pickle_hash = Column(Text)
    __tablename__ = 'dag_pickle'

    def __init__(self, dag):
        self.dag_id = dag.dag_id
        if hasattr(dag, 'template_env'):
            dag.template_env = None
        self.pickle_hash = hash(dag)
        self.pickle = dag