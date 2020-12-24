# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/data/unicode_test_data.py
# Compiled at: 2019-05-15 12:58:52
# Size of source mod 2**32: 4192 bytes
import datetime, json, random, pandas as pd
from sqlalchemy import Date, Float, String
from superset import db
import superset.utils as utils
from .helpers import config, Dash, get_example_data, get_slice_json, merge_slice, Slice, TBL, update_slice_ids

def load_unicode_test_data():
    """Loading unicode test dataset from a csv file in the repo"""
    data = get_example_data('unicode_utf8_unixnl_test.csv',
      is_gzip=False, make_bytes=True)
    df = pd.read_csv(data, encoding='utf-8')
    df['dttm'] = datetime.datetime.now().date()
    df['value'] = [random.randint(1, 100) for _ in range(len(df))]
    df.to_sql('unicode_test',
      (db.engine),
      if_exists='replace',
      chunksize=500,
      dtype={'phrase':String(500), 
     'short_phrase':String(10), 
     'with_missing':String(100), 
     'dttm':Date(), 
     'value':Float()},
      index=False)
    print('Done loading table!')
    print('--------------------------------------------------------------------------------')
    print('Creating table [unicode_test] reference')
    obj = db.session.query(TBL).filter_by(table_name='unicode_test').first()
    if not obj:
        obj = TBL(table_name='unicode_test')
    obj.main_dttm_col = 'dttm'
    obj.database = utils.get_or_create_main_db()
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {'granularity_sqla':'dttm', 
     'groupby':[],  'metric':'sum__value', 
     'row_limit':config.get('ROW_LIMIT'), 
     'since':'100 years ago', 
     'until':'now', 
     'where':'', 
     'viz_type':'word_cloud', 
     'size_from':'10', 
     'series':'short_phrase', 
     'size_to':'70', 
     'rotation':'square', 
     'limit':'100'}
    print('Creating a slice')
    slc = Slice(slice_name='Unicode Cloud',
      viz_type='word_cloud',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    print('Creating a dashboard')
    dash = db.session.query(Dash).filter_by(dashboard_title='Unicode Test').first()
    if not dash:
        dash = Dash()
    js = '{\n    "CHART-Hkx6154FEm": {\n        "children": [],\n        "id": "CHART-Hkx6154FEm",\n        "meta": {\n            "chartId": 2225,\n            "height": 30,\n            "sliceName": "slice 1",\n            "width": 4\n        },\n        "type": "CHART"\n    },\n    "GRID_ID": {\n        "children": [\n            "ROW-SyT19EFEQ"\n        ],\n        "id": "GRID_ID",\n        "type": "GRID"\n    },\n    "ROOT_ID": {\n        "children": [\n            "GRID_ID"\n        ],\n        "id": "ROOT_ID",\n        "type": "ROOT"\n    },\n    "ROW-SyT19EFEQ": {\n        "children": [\n            "CHART-Hkx6154FEm"\n        ],\n        "id": "ROW-SyT19EFEQ",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "DASHBOARD_VERSION_KEY": "v2"\n}\n    '
    dash.dashboard_title = 'Unicode Test'
    pos = json.loads(js)
    update_slice_ids(pos, [slc])
    dash.position_json = json.dumps(pos, indent=4)
    dash.slug = 'unicode-test'
    dash.slices = [slc]
    db.session.merge(dash)
    db.session.commit()