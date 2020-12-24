# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/migrations/versions/6e96a59344a4_make_taskinstance_pool_not_nullable.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4083 bytes
"""Make TaskInstance.pool not nullable

Revision ID: 6e96a59344a4
Revises: 939bb1e647c8
Create Date: 2019-06-13 21:51:32.878437

"""
from alembic import op
import dill, sqlalchemy as sa
from sqlalchemy import Column, Float, Integer, PickleType, String
from sqlalchemy.ext.declarative import declarative_base
from airflow.utils.sqlalchemy import UtcDateTime
revision = '6e96a59344a4'
down_revision = '939bb1e647c8'
branch_labels = None
depends_on = None
Base = declarative_base()
ID_LEN = 250

class TaskInstance(Base):
    __doc__ = "\n    Task instances store the state of a task instance. This table is the\n    authority and single source of truth around what tasks have run and the\n    state they are in.\n\n    The SqlAlchemy model doesn't have a SqlAlchemy foreign key to the task or\n    dag model deliberately to have more control over transactions.\n\n    Database transactions on this table should insure double triggers and\n    any confusion around what task instances are or aren't ready to run\n    even while multiple schedulers may be firing task instances.\n    "
    __tablename__ = 'task_instance'
    task_id = Column((String(ID_LEN)), primary_key=True)
    dag_id = Column((String(ID_LEN)), primary_key=True)
    execution_date = Column(UtcDateTime, primary_key=True)
    start_date = Column(UtcDateTime)
    end_date = Column(UtcDateTime)
    duration = Column(Float)
    state = Column(String(20))
    _try_number = Column('try_number', Integer, default=0)
    max_tries = Column(Integer)
    hostname = Column(String(1000))
    unixname = Column(String(1000))
    job_id = Column(Integer)
    pool = Column((String(50)), nullable=False)
    queue = Column(String(256))
    priority_weight = Column(Integer)
    operator = Column(String(1000))
    queued_dttm = Column(UtcDateTime)
    pid = Column(Integer)
    executor_config = Column(PickleType(pickler=dill))


def upgrade():
    """
    Make TaskInstance.pool field not nullable.
    """
    session = sa.orm.session.Session(bind=(op.get_bind()))
    session.query(TaskInstance).filter(TaskInstance.pool.is_(None)).update({TaskInstance.pool: 'default_pool'},
      synchronize_session=False)
    if not op.get_context().environment_context.is_transactional_ddl():
        session.commit()
    with op.batch_alter_table('task_instance') as (batch_op):
        batch_op.alter_column(column_name='pool',
          type_=(sa.String(50)),
          nullable=False)


def downgrade():
    """
    Make TaskInstance.pool field nullable.
    """
    with op.batch_alter_table('task_instance') as (batch_op):
        batch_op.alter_column(column_name='pool',
          type_=(sa.String(50)),
          nullable=True)
    session = sa.orm.session.Session(bind=(op.get_bind()))
    session.query(TaskInstance).filter(TaskInstance.pool == 'default_pool').update({TaskInstance.pool: None},
      synchronize_session=False)
    if not op.get_context().environment_context.is_transactional_ddl():
        session.commit()