# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\bf706ae5eb46_cal_heatmap_metric_to_metrics.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 2209 bytes
"""cal_heatmap_metric_to_metrics

Revision ID: bf706ae5eb46
Revises: f231d82b9b26
Create Date: 2018-04-10 11:19:47.621878

"""
import json
from alembic import op
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()
revision = 'bf706ae5eb46'
down_revision = 'f231d82b9b26'

class Slice(Base):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    datasource_type = Column(String(200))
    viz_type = Column(String(200))
    slice_name = Column(String(200))
    params = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    slices = session.query(Slice).filter_by(viz_type='cal_heatmap').all()
    slice_len = len(slices)
    for i, slc in enumerate(slices):
        try:
            params = json.loads(slc.params or '{}')
            params['metrics'] = [params.get('metric')]
            del params['metric']
            slc.params = json.dumps(params, indent=2, sort_keys=True)
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