# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/misc_dashboard.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 5764 bytes
import json, textwrap
from superset import db
from superset.models.dashboard import Dashboard
from superset.models.slice import Slice
from .helpers import misc_dash_slices, update_slice_ids
DASH_SLUG = 'misc_charts'

def load_misc_dashboard():
    """Loading a dashboard featuring misc charts"""
    print('Creating the dashboard')
    db.session.expunge_all()
    dash = db.session.query(Dashboard).filter_by(slug=DASH_SLUG).first()
    if not dash:
        dash = Dashboard()
    js = textwrap.dedent('{\n    "CHART-BkeVbh8ANQ": {\n        "children": [],\n        "id": "CHART-BkeVbh8ANQ",\n        "meta": {\n            "chartId": 4004,\n            "height": 34,\n            "sliceName": "Multi Line",\n            "width": 8\n        },\n        "type": "CHART"\n    },\n    "CHART-H1HYNzEANX": {\n        "children": [],\n        "id": "CHART-H1HYNzEANX",\n        "meta": {\n            "chartId": 3940,\n            "height": 50,\n            "sliceName": "Energy Sankey",\n            "width": 6\n        },\n        "type": "CHART"\n    },\n    "CHART-HJOYVMV0E7": {\n        "children": [],\n        "id": "CHART-HJOYVMV0E7",\n        "meta": {\n            "chartId": 3969,\n            "height": 63,\n            "sliceName": "Mapbox Long/Lat",\n            "width": 6\n        },\n        "type": "CHART"\n    },\n    "CHART-S1WYNz4AVX": {\n        "children": [],\n        "id": "CHART-S1WYNz4AVX",\n        "meta": {\n            "chartId": 3989,\n            "height": 25,\n            "sliceName": "Parallel Coordinates",\n            "width": 4\n        },\n        "type": "CHART"\n    },\n    "CHART-r19KVMNCE7": {\n        "children": [],\n        "id": "CHART-r19KVMNCE7",\n        "meta": {\n            "chartId": 3971,\n            "height": 34,\n            "sliceName": "Calendar Heatmap multiformat 0",\n            "width": 4\n        },\n        "type": "CHART"\n    },\n    "CHART-rJ4K4GV04Q": {\n        "children": [],\n        "id": "CHART-rJ4K4GV04Q",\n        "meta": {\n            "chartId": 3941,\n            "height": 63,\n            "sliceName": "Energy Force Layout",\n            "width": 6\n        },\n        "type": "CHART"\n    },\n    "CHART-rkgF4G4A4X": {\n        "children": [],\n        "id": "CHART-rkgF4G4A4X",\n        "meta": {\n            "chartId": 3970,\n            "height": 25,\n            "sliceName": "Birth in France by department in 2016",\n            "width": 8\n        },\n        "type": "CHART"\n    },\n    "CHART-rywK4GVR4X": {\n        "children": [],\n        "id": "CHART-rywK4GVR4X",\n        "meta": {\n            "chartId": 3942,\n            "height": 50,\n            "sliceName": "Heatmap",\n            "width": 6\n        },\n        "type": "CHART"\n    },\n    "COLUMN-ByUFVf40EQ": {\n        "children": [\n            "CHART-rywK4GVR4X",\n            "CHART-HJOYVMV0E7"\n        ],\n        "id": "COLUMN-ByUFVf40EQ",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT",\n            "width": 6\n        },\n        "type": "COLUMN"\n    },\n    "COLUMN-rkmYVGN04Q": {\n        "children": [\n            "CHART-rJ4K4GV04Q",\n            "CHART-H1HYNzEANX"\n        ],\n        "id": "COLUMN-rkmYVGN04Q",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT",\n            "width": 6\n        },\n        "type": "COLUMN"\n    },\n    "GRID_ID": {\n        "children": [\n            "ROW-SytNzNA4X",\n            "ROW-S1MK4M4A4X",\n            "ROW-HkFFEzVRVm"\n        ],\n        "id": "GRID_ID",\n        "type": "GRID"\n    },\n    "HEADER_ID": {\n        "id": "HEADER_ID",\n        "meta": {\n            "text": "Misc Charts"\n        },\n        "type": "HEADER"\n    },\n    "ROOT_ID": {\n        "children": [\n            "GRID_ID"\n        ],\n        "id": "ROOT_ID",\n        "type": "ROOT"\n    },\n    "ROW-HkFFEzVRVm": {\n        "children": [\n            "CHART-r19KVMNCE7",\n            "CHART-BkeVbh8ANQ"\n        ],\n        "id": "ROW-HkFFEzVRVm",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "ROW-S1MK4M4A4X": {\n        "children": [\n            "COLUMN-rkmYVGN04Q",\n            "COLUMN-ByUFVf40EQ"\n        ],\n        "id": "ROW-S1MK4M4A4X",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "ROW-SytNzNA4X": {\n        "children": [\n            "CHART-rkgF4G4A4X",\n            "CHART-S1WYNz4AVX"\n        ],\n        "id": "ROW-SytNzNA4X",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "DASHBOARD_VERSION_KEY": "v2"\n}\n    ')
    pos = json.loads(js)
    slices = db.session.query(Slice).filter(Slice.slice_name.in_(misc_dash_slices)).all()
    slices = sorted(slices, key=(lambda x: x.id))
    update_slice_ids(pos, slices)
    dash.dashboard_title = 'Misc Charts'
    dash.position_json = json.dumps(pos, indent=4)
    dash.slug = DASH_SLUG
    dash.slices = slices
    db.session.merge(dash)
    db.session.commit()