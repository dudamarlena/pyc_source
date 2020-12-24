# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/migrations/versions/80aa3f04bc82_add_parent_ids_in_dashboard_layout.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 3646 bytes
"""Add Parent ids in dashboard layout metadata

Revision ID: 80aa3f04bc82
Revises: 45e7da7cfeba
Create Date: 2019-04-09 16:27:03.392872

"""
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
    __doc__ = 'Declarative class to do query in upgrade'
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    position_json = Column(Text)


def add_parent_ids(node, layout):
    if node:
        current_id = node.get('id')
        parents = list(node.get('parents') or [])
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
            layout = json.loads(dashboard.position_json or '{}')
            if layout:
                if layout['ROOT_ID']:
                    add_parent_ids(layout['ROOT_ID'], layout)
            dashboard.position_json = json.dumps(layout,
              indent=None, separators=(',', ':'), sort_keys=True)
            session.merge(dashboard)
        except Exception as e:
            logging.exception(e)

    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        print('remove parents from dashboard layout, id = {} ({}/{}) >>>>'.format(dashboard.id, i + 1, len(dashboards)))
        try:
            layout = json.loads(dashboard.position_json or '{}')
            for key, item in layout.items():
                if not isinstance(item, dict):
                    pass
                else:
                    item.pop('parents', None)
                    layout[key] = item

            dashboard.position_json = json.dumps(layout,
              indent=None, separators=(',', ':'), sort_keys=True)
            session.merge(dashboard)
        except Exception as e:
            logging.exception(e)

    session.commit()
    session.close()