# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/bddc498dd179_adhoc_filters.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2322 bytes
__doc__ = 'adhoc filters\n\nRevision ID: bddc498dd179\nRevises: afb7730f6a9c\nCreate Date: 2018-06-13 14:54:47.086507\n\n'
revision = 'bddc498dd179'
down_revision = '80a67c5192fa'
import json, uuid
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