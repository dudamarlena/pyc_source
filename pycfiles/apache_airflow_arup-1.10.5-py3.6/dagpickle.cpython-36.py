# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/dagpickle.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 1940 bytes
import dill
from sqlalchemy import Column, Integer, PickleType, Text
from airflow.models.base import Base
from airflow.utils import timezone
from airflow.utils.sqlalchemy import UtcDateTime

class DagPickle(Base):
    __doc__ = '\n    Dags can originate from different places (user repos, master repo, ...)\n    and also get executed in different places (different executors). This\n    object represents a version of a DAG and becomes a source of truth for\n    a BackfillJob execution. A pickle is a native python serialized object,\n    and in this case gets stored in the database for the duration of the job.\n\n    The executors pick up the DagPickle id and read the dag definition from\n    the database.\n    '
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