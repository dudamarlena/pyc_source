# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/data/energy.py
# Compiled at: 2019-05-15 12:58:52
# Size of source mod 2**32: 4249 bytes
"""Loads datasets, dashboards and slices in a new superset instance"""
import textwrap, pandas as pd
from sqlalchemy import Float, String
from superset import db
from superset.connectors.sqla.models import SqlMetric
import superset.utils as utils
from .helpers import DATA_FOLDER, get_example_data, merge_slice, misc_dash_slices, Slice, TBL

def load_energy():
    """Loads an energy related dataset to use with sankey and graphs"""
    tbl_name = 'energy_usage'
    data = get_example_data('energy.json.gz')
    pdf = pd.read_json(data)
    pdf.to_sql(tbl_name,
      (db.engine),
      if_exists='replace',
      chunksize=500,
      dtype={'source':String(255), 
     'target':String(255), 
     'value':Float()},
      index=False)
    print('Creating table [wb_health_population] reference')
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = 'Energy consumption'
    tbl.database = utils.get_or_create_main_db()
    if not any((col.metric_name == 'sum__value' for col in tbl.metrics)):
        tbl.metrics.append(SqlMetric(metric_name='sum__value',
          expression='SUM(value)'))
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    slc = Slice(slice_name='Energy Sankey',
      viz_type='sankey',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(textwrap.dedent('        {\n            "collapsed_fieldsets": "",\n            "groupby": [\n                "source",\n                "target"\n            ],\n            "having": "",\n            "metric": "sum__value",\n            "row_limit": "5000",\n            "slice_name": "Energy Sankey",\n            "viz_type": "sankey",\n            "where": ""\n        }\n        ')))
    misc_dash_slices.add(slc.slice_name)
    merge_slice(slc)
    slc = Slice(slice_name='Energy Force Layout',
      viz_type='directed_force',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(textwrap.dedent('        {\n            "charge": "-500",\n            "collapsed_fieldsets": "",\n            "groupby": [\n                "source",\n                "target"\n            ],\n            "having": "",\n            "link_length": "200",\n            "metric": "sum__value",\n            "row_limit": "5000",\n            "slice_name": "Force",\n            "viz_type": "directed_force",\n            "where": ""\n        }\n        ')))
    misc_dash_slices.add(slc.slice_name)
    merge_slice(slc)
    slc = Slice(slice_name='Heatmap',
      viz_type='heatmap',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(textwrap.dedent('        {\n            "all_columns_x": "source",\n            "all_columns_y": "target",\n            "canvas_image_rendering": "pixelated",\n            "collapsed_fieldsets": "",\n            "having": "",\n            "linear_color_scheme": "blue_white_yellow",\n            "metric": "sum__value",\n            "normalize_across": "heatmap",\n            "slice_name": "Heatmap",\n            "viz_type": "heatmap",\n            "where": "",\n            "xscale_interval": "1",\n            "yscale_interval": "1"\n        }\n        ')))
    misc_dash_slices.add(slc.slice_name)
    merge_slice(slc)