# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/bf706ae5eb46_cal_heatmap_metric_to_metrics.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2209 bytes
__doc__ = 'cal_heatmap_metric_to_metrics\n\nRevision ID: bf706ae5eb46\nRevises: f231d82b9b26\nCreate Date: 2018-04-10 11:19:47.621878\n\n'
import json
from alembic import op
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()
revision = 'bf706ae5eb46'
down_revision = 'f231d82b9b26'

class Slice(Base):
    """Slice"""
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
            params = json.loads(slc.params or )
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