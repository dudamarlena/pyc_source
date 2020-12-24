# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/bddc498dd179_adhoc_filters.py
# Compiled at: 2018-08-15 11:21:52
"""adhoc filters

Revision ID: bddc498dd179
Revises: afb7730f6a9c
Create Date: 2018-06-13 14:54:47.086507

"""
revision = 'bddc498dd179'
down_revision = '80a67c5192fa'
from collections import defaultdict
import json, uuid
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text
from superset import db
from superset import utils
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            params = json.loads(slc.params)
            utils.convert_legacy_filters_into_adhoc(params)
            slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).all():
        try:
            params = json.loads(slc.params)
            utils.split_adhoc_filters_into_base_filters(params)
            if 'adhoc_filters' in params:
                del params['adhoc_filters']
            slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()