# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/random_time_series.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 2655 bytes
import pandas as pd
from sqlalchemy import DateTime
from superset import db
from superset.models.slice import Slice
import superset.utils as utils
from .helpers import config, get_example_data, get_slice_json, merge_slice, TBL

def load_random_time_series_data(only_metadata=False, force=False):
    """Loading random time series data from a zip file in the repo"""
    tbl_name = 'random_time_series'
    database = utils.get_example_database()
    table_exists = database.has_table_by_name(tbl_name)
    if not only_metadata:
        if not table_exists or force:
            data = get_example_data('random_time_series.json.gz')
            pdf = pd.read_json(data)
            pdf.ds = pd.to_datetime((pdf.ds), unit='s')
            pdf.to_sql(tbl_name,
              (database.get_sqla_engine()),
              if_exists='replace',
              chunksize=500,
              dtype={'ds': DateTime},
              index=False)
            print('Done loading table!')
            print('--------------------------------------------------------------------------------')
    print(f"Creating table [{tbl_name}] reference")
    obj = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not obj:
        obj = TBL(table_name=tbl_name)
    obj.main_dttm_col = 'ds'
    obj.database = database
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {'granularity_sqla':'day', 
     'row_limit':config['ROW_LIMIT'], 
     'since':'1 year ago', 
     'until':'now', 
     'metric':'count', 
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