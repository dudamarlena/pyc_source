# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/eca4694defa7_sqllab_setting_defaults.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1624 bytes
__doc__ = 'sqllab_setting_defaults\n\nRevision ID: eca4694defa7\nRevises: 5e4a03ef0bf0\nCreate Date: 2016-09-22 11:31:50.543820\n\n'
from alembic import op
from sqlalchemy import Boolean, Column, Integer
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = 'eca4694defa7'
down_revision = '5e4a03ef0bf0'
Base = declarative_base()

class Database(Base):
    """Database"""
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