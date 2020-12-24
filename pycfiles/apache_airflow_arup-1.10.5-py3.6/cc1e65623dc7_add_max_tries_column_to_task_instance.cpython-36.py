# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/cc1e65623dc7_add_max_tries_column_to_task_instance.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 5146 bytes
"""add max tries column to task instance

Revision ID: cc1e65623dc7
Revises: 127d2bf2dfa7
Create Date: 2017-06-19 16:53:12.851141

"""
from alembic import op
import sqlalchemy as sa
from airflow import settings
from airflow.models import DagBag
from sqlalchemy import Column, Integer, String
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.ext.declarative import declarative_base
revision = 'cc1e65623dc7'
down_revision = '127d2bf2dfa7'
branch_labels = None
depends_on = None
Base = declarative_base()
BATCH_SIZE = 5000
ID_LEN = 250

class TaskInstance(Base):
    __tablename__ = 'task_instance'
    task_id = Column((String(ID_LEN)), primary_key=True)
    dag_id = Column((String(ID_LEN)), primary_key=True)
    execution_date = Column((sa.DateTime), primary_key=True)
    max_tries = Column(Integer)
    try_number = Column(Integer, default=0)


def upgrade():
    op.add_column('task_instance', sa.Column('max_tries', (sa.Integer), server_default='-1'))
    connection = op.get_bind()
    inspector = Inspector.from_engine(connection)
    tables = inspector.get_table_names()
    if 'task_instance' in tables:
        sessionmaker = sa.orm.sessionmaker()
        session = sessionmaker(bind=connection)
        dagbag = DagBag(settings.DAGS_FOLDER)
        query = session.query(sa.func.count(TaskInstance.max_tries)).filter(TaskInstance.max_tries == -1)
        while query.scalar():
            tis = session.query(TaskInstance).filter(TaskInstance.max_tries == -1).limit(BATCH_SIZE).all()
            for ti in tis:
                dag = dagbag.get_dag(ti.dag_id)
                if not dag or not dag.has_task(ti.task_id):
                    ti.max_tries = ti.try_number
                else:
                    task = dag.get_task(ti.task_id)
                    if task.retries:
                        ti.max_tries = task.retries
                    else:
                        ti.max_tries = ti.try_number
                session.merge(ti)

            session.commit()

        session.commit()


def downgrade():
    engine = settings.engine
    if engine.dialect.has_table(engine, 'task_instance'):
        connection = op.get_bind()
        sessionmaker = sa.orm.sessionmaker()
        session = sessionmaker(bind=connection)
        dagbag = DagBag(settings.DAGS_FOLDER)
        query = session.query(sa.func.count(TaskInstance.max_tries)).filter(TaskInstance.max_tries != -1)
        while query.scalar():
            tis = session.query(TaskInstance).filter(TaskInstance.max_tries != -1).limit(BATCH_SIZE).all()
            for ti in tis:
                dag = dagbag.get_dag(ti.dag_id)
                if not dag or not dag.has_task(ti.task_id):
                    ti.try_number = 0
                else:
                    task = dag.get_task(ti.task_id)
                    ti.try_number = max(0, task.retries - (ti.max_tries - ti.try_number))
                ti.max_tries = -1
                session.merge(ti)

            session.commit()

        session.commit()
    op.drop_column('task_instance', 'max_tries')