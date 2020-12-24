# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/eca4694defa7_sqllab_setting_defaults.py
# Compiled at: 2018-08-15 11:21:52
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
    """An ORM object that stores Database related information"""
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