# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: f:\pythonfile\hand_superset\superset\migrations\versions\7fcdcde0761c_.py
# Compiled at: 2019-08-01 07:27:28
# Size of source mod 2**32: 2656 bytes
"""Reduce position_json size by remove extra space and component id prefix

Revision ID: 7fcdcde0761c
Revises: c18bd4186f15
Create Date: 2018-08-01 11:47:02.233971

"""
import json, re
from alembic import op
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '7fcdcde0761c'
down_revision = 'c18bd4186f15'
Base = declarative_base()

class Dashboard(Base):
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'dashboards'
    id = sa.Column((sa.Integer), primary_key=True)
    dashboard_title = sa.Column(sa.String(500))
    position_json = sa.Column(sa.Text)


def is_v2_dash(positions):
    return isinstance(positions, dict) and positions.get('DASHBOARD_VERSION_KEY') == 'v2'


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        original_text = dashboard.position_json or ''
        position_json = json.loads(original_text or '{}')
        if is_v2_dash(position_json):
            text = json.dumps(position_json,
              indent=None, separators=(',', ':'), sort_keys=True)
            text = re.sub('DASHBOARD_(?!VERSION)', '', text)
            text = text.replace('_TYPE', '')
            dashboard.position_json = text
            print('dash id:{} position_json size from {} to {}'.format(dashboard.id, len(original_text), len(text)))
            session.merge(dashboard)
            session.commit()


def downgrade():
    pass