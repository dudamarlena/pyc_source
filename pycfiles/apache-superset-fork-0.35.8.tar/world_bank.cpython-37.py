# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/world_bank.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 16224 bytes
"""Loads datasets, dashboards and slices in a new superset instance"""
import json, os, textwrap, pandas as pd
from sqlalchemy import DateTime, String
from sqlalchemy.sql import column
from superset import db
from superset.connectors.sqla.models import SqlMetric
from superset.models.dashboard import Dashboard
from superset.models.slice import Slice
import superset.utils as utils
from .helpers import config, EXAMPLES_FOLDER, get_example_data, get_slice_json, merge_slice, misc_dash_slices, TBL, update_slice_ids

def load_world_bank_health_n_pop(only_metadata=False, force=False):
    """Loads the world bank health dataset, slices and a dashboard"""
    tbl_name = 'wb_health_population'
    database = utils.get_example_database()
    table_exists = database.has_table_by_name(tbl_name)
    if not only_metadata:
        if not table_exists or force:
            data = get_example_data('countries.json.gz')
            pdf = pd.read_json(data)
            pdf.columns = [col.replace('.', '_') for col in pdf.columns]
            pdf.year = pd.to_datetime(pdf.year)
            pdf.to_sql(tbl_name,
              (database.get_sqla_engine()),
              if_exists='replace',
              chunksize=50,
              dtype={'year':DateTime(), 
             'country_code':String(3), 
             'country_name':String(255), 
             'region':String(255)},
              index=False)
    print('Creating table [wb_health_population] reference')
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = utils.readfile(os.path.join(EXAMPLES_FOLDER, 'countries.md'))
    tbl.main_dttm_col = 'year'
    tbl.database = database
    tbl.filter_select_enabled = True
    metrics = [
     'sum__SP_POP_TOTL',
     'sum__SH_DYN_AIDS',
     'sum__SH_DYN_AIDS',
     'sum__SP_RUR_TOTL_ZS',
     'sum__SP_DYN_LE00_IN',
     'sum__SP_RUR_TOTL']
    for metric in metrics:
        if not any((col.metric_name == metric for col in tbl.metrics)):
            aggr_func = metric[:3]
            col = str(column(metric[5:]).compile(db.engine))
            tbl.metrics.append(SqlMetric(metric_name=metric, expression=f"{aggr_func}({col})"))

    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    defaults = {'compare_lag':'10', 
     'compare_suffix':'o10Y', 
     'limit':'25', 
     'granularity_sqla':'year', 
     'groupby':[],  'metric':'sum__SP_POP_TOTL', 
     'metrics':[
      'sum__SP_POP_TOTL'], 
     'row_limit':config['ROW_LIMIT'], 
     'since':'2014-01-01', 
     'until':'2014-01-02', 
     'time_range':'2014-01-01 : 2014-01-02', 
     'markup_type':'markdown', 
     'country_fieldtype':'cca3', 
     'secondary_metric':{'aggregate':'SUM', 
      'column':{'column_name':'SP_RUR_TOTL', 
       'optionName':'_col_SP_RUR_TOTL', 
       'type':'DOUBLE'}, 
      'expressionType':'SIMPLE', 
      'hasCustomLabel':True, 
      'label':'Rural Population'}, 
     'entity':'country_code', 
     'show_bubbles':True}
    print('Creating slices')
    slices = [
     Slice(slice_name='Region Filter',
       viz_type='filter_box',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='filter_box',
       date_filter=False,
       filter_configs=[
      {'asc':False, 
       'clearable':True, 
       'column':'region', 
       'key':'2s98dfu', 
       'metric':'sum__SP_POP_TOTL', 
       'multiple':True},
      {'asc':False, 
       'clearable':True, 
       'key':'li3j2lk', 
       'column':'country_name', 
       'metric':'sum__SP_POP_TOTL', 
       'multiple':True}])),
     Slice(slice_name="World's Population",
       viz_type='big_number',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       since='2000',
       viz_type='big_number',
       compare_lag='10',
       metric='sum__SP_POP_TOTL',
       compare_suffix='over 10Y')),
     Slice(slice_name='Most Populated Countries',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='table',
       metrics=[
      'sum__SP_POP_TOTL'],
       groupby=[
      'country_name'])),
     Slice(slice_name='Growth Rate',
       viz_type='line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='line',
       since='1960-01-01',
       metrics=[
      'sum__SP_POP_TOTL'],
       num_period_compare='10',
       groupby=[
      'country_name'])),
     Slice(slice_name='% Rural',
       viz_type='world_map',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='world_map',
       metric='sum__SP_RUR_TOTL_ZS',
       num_period_compare='10')),
     Slice(slice_name='Life Expectancy VS Rural %',
       viz_type='bubble',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='bubble',
       since='2011-01-01',
       until='2011-01-02',
       series='region',
       limit=0,
       entity='country_name',
       x='sum__SP_RUR_TOTL_ZS',
       y='sum__SP_DYN_LE00_IN',
       size='sum__SP_POP_TOTL',
       max_bubble_size='50',
       adhoc_filters=[
      {'clause':'WHERE', 
       'expressionType':'SIMPLE', 
       'filterOptionName':'2745eae5', 
       'comparator':[
        'TCA',
        'MNP',
        'DMA',
        'MHL',
        'MCO',
        'SXM',
        'CYM',
        'TUV',
        'IMY',
        'KNA',
        'ASM',
        'ADO',
        'AMA',
        'PLW'], 
       'operator':'not in', 
       'subject':'country_code'}])),
     Slice(slice_name='Rural Breakdown',
       viz_type='sunburst',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='sunburst',
       groupby=[
      'region', 'country_name'],
       since='2011-01-01',
       until='2011-01-01')),
     Slice(slice_name="World's Pop Growth",
       viz_type='area',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       since='1960-01-01',
       until='now',
       viz_type='area',
       groupby=[
      'region'])),
     Slice(slice_name='Box plot',
       viz_type='box_plot',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       since='1960-01-01',
       until='now',
       whisker_options='Min/max (no outliers)',
       x_ticks_layout='staggered',
       viz_type='box_plot',
       groupby=[
      'region'])),
     Slice(slice_name='Treemap',
       viz_type='treemap',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       since='1960-01-01',
       until='now',
       viz_type='treemap',
       metrics=[
      'sum__SP_POP_TOTL'],
       groupby=[
      'region', 'country_code'])),
     Slice(slice_name='Parallel Coordinates',
       viz_type='para',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       since='2011-01-01',
       until='2011-01-01',
       viz_type='para',
       limit=100,
       metrics=[
      'sum__SP_POP_TOTL', 'sum__SP_RUR_TOTL_ZS', 'sum__SH_DYN_AIDS'],
       secondary_metric='sum__SP_POP_TOTL',
       series='country_name'))]
    misc_dash_slices.add(slices[(-1)].slice_name)
    for slc in slices:
        merge_slice(slc)

    print("Creating a World's Health Bank dashboard")
    dash_name = "World Bank's Data"
    slug = 'world_health'
    dash = db.session.query(Dashboard).filter_by(slug=slug).first()
    if not dash:
        dash = Dashboard()
    dash.published = True
    js = textwrap.dedent('{\n    "CHART-36bfc934": {\n        "children": [],\n        "id": "CHART-36bfc934",\n        "meta": {\n            "chartId": 40,\n            "height": 25,\n            "sliceName": "Region Filter",\n            "width": 2\n        },\n        "type": "CHART"\n    },\n    "CHART-37982887": {\n        "children": [],\n        "id": "CHART-37982887",\n        "meta": {\n            "chartId": 41,\n            "height": 25,\n            "sliceName": "World\'s Population",\n            "width": 2\n        },\n        "type": "CHART"\n    },\n    "CHART-17e0f8d8": {\n        "children": [],\n        "id": "CHART-17e0f8d8",\n        "meta": {\n            "chartId": 42,\n            "height": 92,\n            "sliceName": "Most Populated Countries",\n            "width": 3\n        },\n        "type": "CHART"\n    },\n    "CHART-2ee52f30": {\n        "children": [],\n        "id": "CHART-2ee52f30",\n        "meta": {\n            "chartId": 43,\n            "height": 38,\n            "sliceName": "Growth Rate",\n            "width": 6\n        },\n        "type": "CHART"\n    },\n    "CHART-2d5b6871": {\n        "children": [],\n        "id": "CHART-2d5b6871",\n        "meta": {\n            "chartId": 44,\n            "height": 52,\n            "sliceName": "% Rural",\n            "width": 7\n        },\n        "type": "CHART"\n    },\n    "CHART-0fd0d252": {\n        "children": [],\n        "id": "CHART-0fd0d252",\n        "meta": {\n            "chartId": 45,\n            "height": 50,\n            "sliceName": "Life Expectancy VS Rural %",\n            "width": 8\n        },\n        "type": "CHART"\n    },\n    "CHART-97f4cb48": {\n        "children": [],\n        "id": "CHART-97f4cb48",\n        "meta": {\n            "chartId": 46,\n            "height": 38,\n            "sliceName": "Rural Breakdown",\n            "width": 3\n        },\n        "type": "CHART"\n    },\n    "CHART-b5e05d6f": {\n        "children": [],\n        "id": "CHART-b5e05d6f",\n        "meta": {\n            "chartId": 47,\n            "height": 50,\n            "sliceName": "World\'s Pop Growth",\n            "width": 4\n        },\n        "type": "CHART"\n    },\n    "CHART-e76e9f5f": {\n        "children": [],\n        "id": "CHART-e76e9f5f",\n        "meta": {\n            "chartId": 48,\n            "height": 50,\n            "sliceName": "Box plot",\n            "width": 4\n        },\n        "type": "CHART"\n    },\n    "CHART-a4808bba": {\n        "children": [],\n        "id": "CHART-a4808bba",\n        "meta": {\n            "chartId": 49,\n            "height": 50,\n            "sliceName": "Treemap",\n            "width": 8\n        },\n        "type": "CHART"\n    },\n    "COLUMN-071bbbad": {\n        "children": [\n            "ROW-1e064e3c",\n            "ROW-afdefba9"\n        ],\n        "id": "COLUMN-071bbbad",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT",\n            "width": 9\n        },\n        "type": "COLUMN"\n    },\n    "COLUMN-fe3914b8": {\n        "children": [\n            "CHART-36bfc934",\n            "CHART-37982887"\n        ],\n        "id": "COLUMN-fe3914b8",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT",\n            "width": 2\n        },\n        "type": "COLUMN"\n    },\n    "GRID_ID": {\n        "children": [\n            "ROW-46632bc2",\n            "ROW-3fa26c5d",\n            "ROW-812b3f13"\n        ],\n        "id": "GRID_ID",\n        "type": "GRID"\n    },\n    "HEADER_ID": {\n        "id": "HEADER_ID",\n        "meta": {\n            "text": "World\'s Bank Data"\n        },\n        "type": "HEADER"\n    },\n    "ROOT_ID": {\n        "children": [\n            "GRID_ID"\n        ],\n        "id": "ROOT_ID",\n        "type": "ROOT"\n    },\n    "ROW-1e064e3c": {\n        "children": [\n            "COLUMN-fe3914b8",\n            "CHART-2d5b6871"\n        ],\n        "id": "ROW-1e064e3c",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "ROW-3fa26c5d": {\n        "children": [\n            "CHART-b5e05d6f",\n            "CHART-0fd0d252"\n        ],\n        "id": "ROW-3fa26c5d",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "ROW-46632bc2": {\n        "children": [\n            "COLUMN-071bbbad",\n            "CHART-17e0f8d8"\n        ],\n        "id": "ROW-46632bc2",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "ROW-812b3f13": {\n        "children": [\n            "CHART-a4808bba",\n            "CHART-e76e9f5f"\n        ],\n        "id": "ROW-812b3f13",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "ROW-afdefba9": {\n        "children": [\n            "CHART-2ee52f30",\n            "CHART-97f4cb48"\n        ],\n        "id": "ROW-afdefba9",\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW"\n    },\n    "DASHBOARD_VERSION_KEY": "v2"\n}\n    ')
    pos = json.loads(js)
    update_slice_ids(pos, slices)
    dash.dashboard_title = dash_name
    dash.position_json = json.dumps(pos, indent=4)
    dash.slug = slug
    dash.slices = slices[:-1]
    db.session.merge(dash)
    db.session.commit()