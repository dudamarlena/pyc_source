# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/models/pool.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3379 bytes
from sqlalchemy import Column, Integer, String, Text
from airflow.models.base import Base
from airflow.utils.state import State
from airflow.utils.db import provide_session

class Pool(Base):
    __tablename__ = 'slot_pool'
    id = Column(Integer, primary_key=True)
    pool = Column((String(50)), unique=True)
    slots = Column(Integer, default=0)
    description = Column(Text)
    DEFAULT_POOL_NAME = 'default_pool'

    def __repr__(self):
        return self.pool

    @staticmethod
    @provide_session
    def get_pool(pool_name, session=None):
        return session.query(Pool).filter(Pool.pool == pool_name).first()

    @staticmethod
    @provide_session
    def get_default_pool(session=None):
        return Pool.get_pool((Pool.DEFAULT_POOL_NAME), session=session)

    def to_json(self):
        return {'id':self.id, 
         'pool':self.pool, 
         'slots':self.slots, 
         'description':self.description}

    @provide_session
    def occupied_slots(self, session):
        """
        Returns the number of slots used by running/queued tasks at the moment.
        """
        from airflow.models.taskinstance import TaskInstance
        return session.query(TaskInstance).filter(TaskInstance.pool == self.pool).filter(TaskInstance.state.in_([State.QUEUED, State.RUNNING])).count()

    @provide_session
    def used_slots(self, session):
        """
        Returns the number of slots used by running tasks at the moment.
        """
        from airflow.models.taskinstance import TaskInstance
        running = session.query(TaskInstance).filter(TaskInstance.pool == self.pool).filter(TaskInstance.state == State.RUNNING).count()
        return running

    @provide_session
    def queued_slots(self, session):
        """
        Returns the number of slots used by queued tasks at the moment.
        """
        from airflow.models.taskinstance import TaskInstance
        return session.query(TaskInstance).filter(TaskInstance.pool == self.pool).filter(TaskInstance.state == State.QUEUED).count()

    @provide_session
    def open_slots(self, session):
        """
        Returns the number of slots open at the moment
        """
        return self.slots - self.occupied_slots(session)