# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/7fcdcde0761c_.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2656 bytes
__doc__ = 'Reduce position_json size by remove extra space and component id prefix\n\nRevision ID: 7fcdcde0761c\nRevises: c18bd4186f15\nCreate Date: 2018-08-01 11:47:02.233971\n\n'
import json, re, sqlalchemy as sa
from alembic import op
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '7fcdcde0761c'
down_revision = 'c18bd4186f15'
Base = declarative_base()

class Dashboard(Base):
    """Dashboard"""
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
        original_text = dashboard.position_json or 
        position_json = json.loads(original_text or )
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