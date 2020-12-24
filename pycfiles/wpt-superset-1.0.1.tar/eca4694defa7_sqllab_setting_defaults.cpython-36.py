# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/eca4694defa7_sqllab_setting_defaults.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 1625 bytes
"""sqllab_setting_defaults

Revision ID: eca4694defa7
Revises: 5e4a03ef0bf0
Create Date: 2016-09-22 11:31:50.543820

"""
from alembic import op
from superset import db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Boolean
revision = 'eca4694defa7'
down_revision = '5e4a03ef0bf0'
Base = declarative_base()

class Database(Base):
    __doc__ = 'An ORM object that stores Database related information'
    __tablename__ = 'dbs'
    id = Column(Integer, primary_key=True)
    allow_run_sync = Column(Boolean, default=True)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for obj in session.query(Database).all():
        obj.allow_run_sync = True

    session.commit()
    session.close()


def downgrade():
    pass