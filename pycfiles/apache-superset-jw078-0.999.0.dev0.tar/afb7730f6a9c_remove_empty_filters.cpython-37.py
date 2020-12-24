# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/afb7730f6a9c_remove_empty_filters.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2055 bytes
__doc__ = 'remove empty filters\n\nRevision ID: afb7730f6a9c\nRevises: c5756bec8b47\nCreate Date: 2018-06-07 09:52:54.535961\n\n'
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
                    params[key] = [x for x in value if x['op'] in ('in', 'not in') if x['val']]

            slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def downgrade():
    pass