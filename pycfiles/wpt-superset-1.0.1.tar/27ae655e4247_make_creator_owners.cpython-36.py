# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/27ae655e4247_make_creator_owners.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 2718 bytes
"""Make creator owners

Revision ID: 27ae655e4247
Revises: d8bc074f7aad
Create Date: 2016-06-27 08:43:52.592242

"""
revision = '27ae655e4247'
down_revision = 'd8bc074f7aad'
from alembic import op
from superset import db
from sqlalchemy.ext.declarative import declarative_base
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy.orm import relationship
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey, Table
Base = declarative_base()

class User(Base):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'ab_user'
    id = Column(Integer, primary_key=True)


slice_user = Table('slice_user', Base.metadata, Column('id', Integer, primary_key=True), Column('user_id', Integer, ForeignKey('ab_user.id')), Column('slice_id', Integer, ForeignKey('slices.id')))
dashboard_user = Table('dashboard_user', Base.metadata, Column('id', Integer, primary_key=True), Column('user_id', Integer, ForeignKey('ab_user.id')), Column('dashboard_id', Integer, ForeignKey('dashboards.id')))

class Slice(Base, AuditMixin):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    owners = relationship('User', secondary=slice_user)


class Dashboard(Base, AuditMixin):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    owners = relationship('User', secondary=dashboard_user)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    objects = session.query(Slice).all()
    objects += session.query(Dashboard).all()
    for obj in objects:
        if obj.created_by:
            if obj.created_by not in obj.owners:
                obj.owners.append(obj.created_by)
        session.commit()

    session.close()


def downgrade():
    pass