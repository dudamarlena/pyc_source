# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/78ee127d0d1d_reconvert_legacy_filters_into_adhoc.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 2080 bytes
"""reconvert legacy filters into adhoc

Revision ID: 78ee127d0d1d
Revises: c2acd2cf3df2
Create Date: 2019-11-06 15:23:26.497876

"""
revision = '78ee127d0d1d'
down_revision = 'c2acd2cf3df2'
import copy, json, logging, uuid
from collections import defaultdict
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
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
        if slc.params:
            try:
                source = json.loads(slc.params)
                target = copy.deepcopy(source)
                convert_legacy_filters_into_adhoc(target)
                if source != target:
                    slc.params = json.dumps(target, sort_keys=True)
            except Exception as ex:
                logging.warn(ex)

    session.commit()
    session.close()


def downgrade():
    pass