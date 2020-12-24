# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/data/random_time_series.py
# Compiled at: 2019-05-15 12:58:52
# Size of source mod 2**32: 2460 bytes
import pandas as pd
from sqlalchemy import DateTime
from superset import db
import superset.utils as utils
from .helpers import config, get_example_data, get_slice_json, merge_slice, Slice, TBL

def load_random_time_series_data():
    """Loading random time series data from a zip file in the repo"""
    data = get_example_data('random_time_series.json.gz')
    pdf = pd.read_json(data)
    pdf.ds = pd.to_datetime((pdf.ds), unit='s')
    pdf.to_sql('random_time_series',
      (db.engine),
      if_exists='replace',
      chunksize=500,
      dtype={'ds': DateTime},
      index=False)
    print('Done loading table!')
    print('--------------------------------------------------------------------------------')
    print('Creating table [random_time_series] reference')
    obj = db.session.query(TBL).filter_by(table_name='random_time_series').first()
    if not obj:
        obj = TBL(table_name='random_time_series')
    obj.main_dttm_col = 'ds'
    obj.database = utils.get_or_create_main_db()
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {'granularity_sqla':'day', 
     'row_limit':config.get('ROW_LIMIT'), 
     'since':'1 year ago', 
     'until':'now', 
     'metric':'count', 
     'where':'', 
     'viz_type':'cal_heatmap', 
     'domain_granularity':'month', 
     'subdomain_granularity':'day'}
    print('Creating a slice')
    slc = Slice(slice_name='Calendar Heatmap',
      viz_type='cal_heatmap',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)