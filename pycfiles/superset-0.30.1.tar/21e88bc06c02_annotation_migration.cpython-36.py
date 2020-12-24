# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/21e88bc06c02_annotation_migration.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 2915 bytes
import json
from alembic import op
from sqlalchemy import Column, Integer, or_, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '21e88bc06c02'
down_revision = '67a6ac9b727b'
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    viz_type = Column(String(250))
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(or_(Slice.viz_type.like('line'), Slice.viz_type.like('bar'))):
        params = json.loads(slc.params)
        layers = params.get('annotation_layers', [])
        if layers:
            new_layers = []
            for layer in layers:
                new_layers.append({'annotationType':'INTERVAL', 
                 'style':'solid', 
                 'name':'Layer {}'.format(layer), 
                 'show':True, 
                 'overrides':{'since':None, 
                  'until':None}, 
                 'value':layer, 
                 'width':1, 
                 'sourceType':'NATIVE'})

            params['annotation_layers'] = new_layers
            slc.params = json.dumps(params)
            session.merge(slc)
            session.commit()

    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(or_(Slice.viz_type.like('line'), Slice.viz_type.like('bar'))):
        params = json.loads(slc.params)
        layers = params.get('annotation_layers', [])
        if layers:
            params['annotation_layers'] = [layer['value'] for layer in layers]
            slc.params = json.dumps(params)
            session.merge(slc)
            session.commit()

    session.close()