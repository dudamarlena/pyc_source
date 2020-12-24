# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/helpers.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 2506 bytes
__doc__ = 'Loads datasets, dashboards and slices in a new superset instance'
import json, os, zlib
from io import BytesIO
from typing import Set
from urllib import request
from superset import app, db
from superset.connectors.connector_registry import ConnectorRegistry
import superset.models as models
from superset.models.slice import Slice
BASE_URL = 'https://github.com/apache-superset/examples-data/blob/master/'
DB = models.Database
TBL = ConnectorRegistry.sources['table']
config = app.config
EXAMPLES_FOLDER = os.path.join(config['BASE_DIR'], 'examples')
misc_dash_slices = set()
misc_dash_slices: Set[str]

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


def get_example_data(filepath, is_gzip=True, make_bytes=False):
    content = request.urlopen(f"{BASE_URL}{filepath}?raw=true").read()
    if is_gzip:
        content = zlib.decompress(content, zlib.MAX_WBITS | 16)
    if make_bytes:
        content = BytesIO(content)
    return content