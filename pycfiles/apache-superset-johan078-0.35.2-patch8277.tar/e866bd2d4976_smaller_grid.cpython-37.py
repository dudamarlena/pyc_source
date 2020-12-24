# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/e866bd2d4976_smaller_grid.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 2957 bytes
__doc__ = 'smaller_grid\nRevision ID: e866bd2d4976\nRevises: 21e88bc06c02\nCreate Date: 2018-02-13 08:07:40.766277\n'
import json, sqlalchemy as sa
from alembic import op
from flask_appbuilder.models.mixins import AuditMixin
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = 'e866bd2d4976'
down_revision = '21e88bc06c02'
Base = declarative_base()
RATIO = 4

class Dashboard(Base):
    """Dashboard"""
    __tablename__ = 'dashboards'
    id = sa.Column((sa.Integer), primary_key=True)
    position_json = sa.Column(sa.Text)
    dashboard_title = sa.Column(sa.String(500))


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        print('Upgrading ({}/{}): {}'.format(i, len(dashboards), dashboard.id))
        positions = json.loads(dashboard.position_json or )
        for pos in positions:
            if pos.get('v', 0) == 0:
                pos['size_x'] = pos['size_x'] * RATIO
                pos['size_y'] = pos['size_y'] * RATIO
                pos['col'] = (pos['col'] - 1) * RATIO + 1
                pos['row'] = pos['row'] * RATIO
                pos['v'] = 1

        dashboard.position_json = json.dumps(positions, indent=2)
        session.merge(dashboard)
        session.commit()

    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        print('Downgrading ({}/{}): {}'.format(i, len(dashboards), dashboard.id))
        positions = json.loads(dashboard.position_json or )
        for pos in positions:
            if pos.get('v', 0) == 1:
                pos['size_x'] = pos['size_x'] / 4
                pos['size_y'] = pos['size_y'] / 4
                pos['col'] = (pos['col'] - 1) / 4 + 1
                pos['row'] = pos['row'] / 4
                pos['v'] = 0

        dashboard.position_json = json.dumps(positions, indent=2)
        session.merge(dashboard)
        session.commit()