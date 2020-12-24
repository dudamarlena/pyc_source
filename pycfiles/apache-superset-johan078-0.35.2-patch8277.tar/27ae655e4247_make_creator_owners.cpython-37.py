# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/27ae655e4247_make_creator_owners.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2735 bytes
__doc__ = 'Make creator owners\n\nRevision ID: 27ae655e4247\nRevises: d8bc074f7aad\nCreate Date: 2016-06-27 08:43:52.592242\n\n'
revision = '27ae655e4247'
down_revision = 'd8bc074f7aad'
from alembic import op
from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from superset import db
Base = declarative_base()

class User(Base):
    """User"""
    __tablename__ = 'ab_user'
    id = Column(Integer, primary_key=True)


slice_user = Table('slice_user', Base.metadata, Column('id', Integer, primary_key=True), Column('user_id', Integer, ForeignKey('ab_user.id')), Column('slice_id', Integer, ForeignKey('slices.id')))
dashboard_user = Table('dashboard_user', Base.metadata, Column('id', Integer, primary_key=True), Column('user_id', Integer, ForeignKey('ab_user.id')), Column('dashboard_id', Integer, ForeignKey('dashboards.id')))

class Slice(Base, AuditMixin):
    """Slice"""
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    owners = relationship('User', secondary=slice_user)


class Dashboard(Base, AuditMixin):
    """Dashboard"""
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