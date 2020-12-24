# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/67a6ac9b727b_update_spatial_params.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 1978 bytes
__doc__ = 'update_spatial_params\n\nRevision ID: 67a6ac9b727b\nRevises: 4736ec66ce19\nCreate Date: 2017-12-08 08:19:21.148775\n\n'
import json
from alembic import op
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '67a6ac9b727b'
down_revision = '4736ec66ce19'
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    viz_type = Column(String(250))
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(Slice.viz_type.like('deck_%')):
        params = json.loads(slc.params)
        if params.get('latitude'):
            params['spatial'] = {'lonCol':params.get('longitude'),  'latCol':params.get('latitude'), 
             'type':'latlong'}
            del params['latitude']
            del params['longitude']
        slc.params = json.dumps(params)
        session.merge(slc)
        session.commit()

    session.close()


def downgrade():
    pass