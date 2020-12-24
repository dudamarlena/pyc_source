# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/moretti/PycharmProjects/incubator-superset/superset/migrations/versions/80a67c5192fa_single_pie_chart_metric.py
# Compiled at: 2018-08-15 11:21:52
"""single pie chart metric

Revision ID: 80a67c5192fa
Revises: afb7730f6a9c
Create Date: 2018-06-14 14:31:06.624370

"""
revision = '80a67c5192fa'
down_revision = 'afb7730f6a9c'
import json
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Text
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