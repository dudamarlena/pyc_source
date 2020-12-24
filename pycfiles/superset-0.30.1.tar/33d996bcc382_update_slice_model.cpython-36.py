# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/33d996bcc382_update_slice_model.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 2352 bytes
"""update slice model

Revision ID: 33d996bcc382
Revises: 41f6a59a61f2
Create Date: 2016-09-07 23:50:59.366779

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '33d996bcc382'
down_revision = '41f6a59a61f2'
Base = declarative_base()

class Slice(Base):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    datasource_id = Column(Integer)
    druid_datasource_id = Column(Integer)
    table_id = Column(Integer)
    datasource_type = Column(String(200))


def upgrade():
    bind = op.get_bind()
    op.add_column('slices', sa.Column('datasource_id', sa.Integer()))
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        if slc.druid_datasource_id:
            slc.datasource_id = slc.druid_datasource_id
        if slc.table_id:
            slc.datasource_id = slc.table_id
        session.merge(slc)
        session.commit()

    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        if slc.datasource_type == 'druid':
            slc.druid_datasource_id = slc.datasource_id
        if slc.datasource_type == 'table':
            slc.table_id = slc.datasource_id
        session.merge(slc)
        session.commit()

    session.close()
    op.drop_column('slices', 'datasource_id')