# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/80a67c5192fa_single_pie_chart_metric.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2425 bytes
__doc__ = 'single pie chart metric\n\nRevision ID: 80a67c5192fa\nRevises: afb7730f6a9c\nCreate Date: 2018-06-14 14:31:06.624370\n\n'
revision = '80a67c5192fa'
down_revision = 'afb7730f6a9c'
import json
from alembic import op
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
Base = declarative_base()

class Slice(Base):
    __tablename__ = 'slices'
    id = Column(Integer, primary_key=True)
    params = Column(Text)
    viz_type = Column(String(250))


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(Slice.viz_type == 'pie').all():
        try:
            params = json.loads(slc.params)
            if 'metrics' in params:
                if params['metrics']:
                    params['metric'] = params['metrics'][0]
                del params['metrics']
                slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    for slc in session.query(Slice).filter(Slice.viz_type == 'pie').all():
        try:
            params = json.loads(slc.params)
            if 'metric' in params:
                if params['metric']:
                    params['metrics'] = [
                     params['metric']]
                del params['metric']
                slc.params = json.dumps(params, sort_keys=True)
        except Exception:
            pass

    session.commit()
    session.close()