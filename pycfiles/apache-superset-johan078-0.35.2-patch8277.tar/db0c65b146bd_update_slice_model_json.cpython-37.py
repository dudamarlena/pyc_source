# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/db0c65b146bd_update_slice_model_json.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2037 bytes
__doc__ = 'update_slice_model_json\n\nRevision ID: db0c65b146bd\nRevises: f18570e03440\nCreate Date: 2017-01-24 12:31:06.541746\n\n'
revision = 'db0c65b146bd'
down_revision = 'f18570e03440'
import json
from alembic import op
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()

class Slice(Base):
    """Slice"""
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    datasource_type = Column(String(200))
    slice_name = Column(String(200))
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    slices = session.query(Slice).all()
    slice_len = len(slices)
    for i, slc in enumerate(slices):
        try:
            d = json.loads(slc.params or )
            slc.params = json.dumps(d, indent=2, sort_keys=True)
            session.merge(slc)
            session.commit()
            print('Upgraded ({}/{}): {}'.format(i, slice_len, slc.slice_name))
        except Exception as e:
            try:
                print(slc.slice_name + ' error: ' + str(e))
            finally:
                e = None
                del e

    session.close()


def downgrade():
    pass