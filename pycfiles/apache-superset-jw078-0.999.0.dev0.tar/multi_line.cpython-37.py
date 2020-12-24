# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/multi_line.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 1977 bytes
import json
from superset import db
from superset.models.slice import Slice
from .birth_names import load_birth_names
from .helpers import merge_slice, misc_dash_slices
from .world_bank import load_world_bank_health_n_pop

def load_multi_line(only_metadata=False):
    load_world_bank_health_n_pop(only_metadata)
    load_birth_names(only_metadata)
    ids = [row.id for row in db.session.query(Slice).filter(Slice.slice_name.in_(['Growth Rate', 'Trends']))]
    slc = Slice(datasource_type='table',
      datasource_id=1,
      slice_name='Multi Line',
      viz_type='line_multi',
      params=(json.dumps({'slice_name':'Multi Line', 
     'viz_type':'line_multi', 
     'line_charts':[
      ids[0]], 
     'line_charts_2':[
      ids[1]], 
     'since':'1970', 
     'until':'1995', 
     'prefix_metric_with_slice_name':True, 
     'show_legend':False, 
     'x_axis_format':'%Y'})))
    misc_dash_slices.add(slc.slice_name)
    merge_slice(slc)