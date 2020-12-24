# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/data/helpers.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 2062 bytes
"""Loads datasets, dashboards and slices in a new superset instance"""
import json, os
from superset import app, db
from superset.connectors.connector_registry import ConnectorRegistry
from superset.models import core as models
DB = models.Database
Slice = models.Slice
Dash = models.Dashboard
TBL = ConnectorRegistry.sources['table']
config = app.config
DATA_FOLDER = os.path.join(config.get('BASE_DIR'), 'data')
misc_dash_slices = set()

def update_slice_ids(layout_dict, slices):
    charts = [component for component in layout_dict.values() if isinstance(component, dict) if component['type'] == 'CHART']
    sorted_charts = sorted(charts, key=(lambda k: k['meta']['chartId']))
    for i, chart_component in enumerate(sorted_charts):
        if i < len(slices):
            chart_component['meta']['chartId'] = int(slices[i].id)


def merge_slice(slc):
    o = db.session.query(Slice).filter_by(slice_name=(slc.slice_name)).first()
    if o:
        db.session.delete(o)
    db.session.add(slc)
    db.session.commit()


def get_slice_json(defaults, **kwargs):
    d = defaults.copy()
    d.update(kwargs)
    return json.dumps(d, indent=4, sort_keys=True)