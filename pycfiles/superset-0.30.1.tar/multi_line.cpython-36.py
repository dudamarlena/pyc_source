# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/examples/multi_line.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 1944 bytes
import json
from superset import db
from .birth_names import load_birth_names
from .helpers import merge_slice, misc_dash_slices, Slice
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