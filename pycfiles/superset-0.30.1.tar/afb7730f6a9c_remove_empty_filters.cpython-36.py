# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/afb7730f6a9c_remove_empty_filters.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 2055 bytes
"""remove empty filters

Revision ID: afb7730f6a9c
Revises: c5756bec8b47
Create Date: 2018-06-07 09:52:54.535961

"""
revision = 'afb7730f6a9c'
down_revision = 'c5756bec8b47'
import json
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
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
            for key in ('filters', 'having_filters', 'extra_filters'):
                value = params.get(key)
                if value:
                    params[key] = [x for x in value if not (x['op'] in ('in', 'not in') and not x['val'])]

            slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def downgrade():
    pass