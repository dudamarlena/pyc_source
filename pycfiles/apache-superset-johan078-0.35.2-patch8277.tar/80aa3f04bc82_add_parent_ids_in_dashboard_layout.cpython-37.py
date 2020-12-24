# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/80aa3f04bc82_add_parent_ids_in_dashboard_layout.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 3646 bytes
__doc__ = 'Add Parent ids in dashboard layout metadata\n\nRevision ID: 80aa3f04bc82\nRevises: 45e7da7cfeba\nCreate Date: 2019-04-09 16:27:03.392872\n\n'
import json, logging, sqlalchemy as sa
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from superset import db
revision = '80aa3f04bc82'
down_revision = '45e7da7cfeba'
Base = declarative_base()

class Dashboard(Base):
    """Dashboard"""
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    position_json = Column(Text)


def add_parent_ids(node, layout):
    if node:
        current_id = node.get('id')
        parents = list(node.get('parents') or )
        child_ids = node.get('children')
        if child_ids:
            if len(child_ids) > 0:
                parents.append(current_id)
                for child_id in child_ids:
                    child_node = layout.get(child_id)
                    child_node['parents'] = parents
                    add_parent_ids(child_node, layout)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        print('adding parents for dashboard layout, id = {} ({}/{}) >>>>'.format(dashboard.id, i + 1, len(dashboards)))
        try:
            layout = json.loads(dashboard.position_json or )
            if layout:
                if layout['ROOT_ID']:
                    add_parent_ids(layout['ROOT_ID'], layout)
            dashboard.position_json = json.dumps(layout,
              indent=None, separators=(',', ':'), sort_keys=True)
            session.merge(dashboard)
        except Exception as e:
            try:
                logging.exception(e)
            finally:
                e = None
                del e

    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        print('remove parents from dashboard layout, id = {} ({}/{}) >>>>'.format(dashboard.id, i + 1, len(dashboards)))
        try:
            layout = json.loads(dashboard.position_json or )
            for key, item in layout.items():
                if not isinstance(item, dict):
                    continue
                item.pop('parents', None)
                layout[key] = item

            dashboard.position_json = json.dumps(layout,
              indent=None, separators=(',', ':'), sort_keys=True)
            session.merge(dashboard)
        except Exception as e:
            try:
                logging.exception(e)
            finally:
                e = None
                del e

    session.commit()
    session.close()