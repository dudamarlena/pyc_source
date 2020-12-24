# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/migrations/versions/4ce8df208545_migrate_time_range_for_default_filters.py
# Compiled at: 2020-01-16 13:27:41
# Size of source mod 2**32: 4235 bytes
__doc__ = 'empty message\n\nRevision ID: 4ce8df208545\nRevises: 55e910a74826\nCreate Date: 2018-11-12 13:31:07.578090\n\n'
import json
from alembic import op
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from superset import db
revision = '4ce8df208545'
down_revision = '55e910a74826'
Base = declarative_base()

class Dashboard(Base):
    """Dashboard"""
    __tablename__ = 'dashboards'
    id = Column(Integer, primary_key=True)
    json_metadata = Column(Text)


def upgrade():
    bind = op.get_bind()
    session = db.Session(bind=bind)
    dashboards = session.query(Dashboard).all()
    for i, dashboard in enumerate(dashboards):
        print('scanning dashboard ({}/{}) >>>>'.format(i + 1, len(dashboards)))
        if dashboard.json_metadata:
            json_metadata = json.loads(dashboard.json_metadata)
            has_update = False
            default_filters = json_metadata.get('default_filters')
            if default_filters:
                if default_filters != '{}':
                    try:
                        filters = json.loads(default_filters)
                        keys = [key for key, val in filters.items() if not val.get('__from') if val.get('__to')]
                        if len(keys):
                            for key in keys:
                                val = filters[key]
                                __from = val.pop('__from', '')
                                __to = val.pop('__to', '')
                                if '__time_range' not in val:
                                    val['__time_range'] = '{} : {}'.format(__from, __to)

                            json_metadata['default_filters'] = json.dumps(filters)
                            has_update = True
                    except Exception:
                        pass

            filter_immune_slice_fields = json_metadata.get('filter_immune_slice_fields')
        if filter_immune_slice_fields:
            keys = [key for key, val in filter_immune_slice_fields.items() if not '__from' in val if '__to' in val]
            if len(keys):
                for key in keys:
                    val = filter_immune_slice_fields[key]
                    if '__from' in val:
                        val.remove('__from')
                    if '__to' in val:
                        val.remove('__to')
                    if '__time_range' not in val:
                        val.append('__time_range')

                json_metadata['filter_immune_slice_fields'] = filter_immune_slice_fields
                has_update = True
            if has_update:
                dashboard.json_metadata = json.dumps(json_metadata)

    session.commit()
    session.close()


def downgrade():
    pass