# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/migrations/versions/bddc498dd179_adhoc_filters.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 2317 bytes
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
from superset.utils.core import convert_legacy_filters_into_adhoc, split_adhoc_filters_into_base_filters
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
            convert_legacy_filters_into_adhoc(params)
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
            split_adhoc_filters_into_base_filters(params)
            if 'adhoc_filters' in params:
                del params['adhoc_filters']
            slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()