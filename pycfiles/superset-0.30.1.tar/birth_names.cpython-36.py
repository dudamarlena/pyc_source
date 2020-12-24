# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maximebeauchemin/code/superset/superset/examples/birth_names.py
# Compiled at: 2019-11-14 17:12:06
# Size of source mod 2**32: 22485 bytes
import json, textwrap, pandas as pd
from sqlalchemy import DateTime, String
from sqlalchemy.sql import column
from superset import db, security_manager
from superset.connectors.sqla.models import SqlMetric, TableColumn
from superset.utils.core import get_example_database
from .helpers import config, Dash, get_example_data, get_slice_json, merge_slice, misc_dash_slices, Slice, TBL, update_slice_ids

def gen_filter(subject, comparator, operator='=='):
    return {'clause':'WHERE', 
     'comparator':comparator, 
     'expressionType':'SIMPLE', 
     'operator':operator, 
     'subject':subject, 
     'fromFormData':True}


def load_data(tbl_name, database):
    pdf = pd.read_json(get_example_data('birth_names.json.gz'))
    pdf.ds = pd.to_datetime((pdf.ds), unit='ms')
    pdf.to_sql(tbl_name,
      (database.get_sqla_engine()),
      if_exists='replace',
      chunksize=500,
      dtype={'ds':DateTime, 
     'gender':String(16), 
     'state':String(10), 
     'name':String(255)},
      index=False)
    print('Done loading table!')
    print('-' * 80)


def load_birth_names(only_metadata=False, force=False):
    """Loading birth name dataset from a zip file in the repo"""
    tbl_name = 'birth_names'
    database = get_example_database()
    table_exists = database.has_table_by_name(tbl_name)
    if not only_metadata:
        if not table_exists or force:
            load_data(tbl_name, database)
    obj = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not obj:
        print(f"Creating table [{tbl_name}] reference")
        obj = TBL(table_name=tbl_name)
        db.session.add(obj)
    obj.main_dttm_col = 'ds'
    obj.database = database
    obj.filter_select_enabled = True
    if not any(col.column_name == 'num_california' for col in obj.columns):
        col_state = str(column('state').compile(db.engine))
        col_num = str(column('num').compile(db.engine))
        obj.columns.append(TableColumn(column_name='num_california',
          expression=f"CASE WHEN {col_state} = 'CA' THEN {col_num} ELSE 0 END"))
    if not any(col.metric_name == 'sum__num' for col in obj.metrics):
        col = str(column('num').compile(db.engine))
        obj.metrics.append(SqlMetric(metric_name='sum__num', expression=f"SUM({col})"))
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    defaults = {'compare_lag':'10', 
     'compare_suffix':'o10Y', 
     'limit':'25', 
     'granularity_sqla':'ds', 
     'groupby':[],  'metric':'sum__num', 
     'metrics':[
      {'expressionType':'SIMPLE', 
       'column':{'column_name':'num', 
        'type':'BIGINT'}, 
       'aggregate':'SUM', 
       'label':'Births', 
       'optionName':'metric_11'}], 
     'row_limit':config['ROW_LIMIT'], 
     'since':'100 years ago', 
     'until':'now', 
     'viz_type':'table', 
     'markup_type':'markdown'}
    admin = security_manager.find_user('admin')
    print('Creating some slices')
    slices = [
     Slice(slice_name='Participants',
       viz_type='big_number',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='big_number',
       granularity_sqla='ds',
       compare_lag='5',
       compare_suffix='over 5Y')),
     Slice(slice_name='Genders',
       viz_type='pie',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults, viz_type='pie', groupby=['gender'])),
     Slice(slice_name='Trends',
       viz_type='line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='line',
       groupby=[
      'name'],
       granularity_sqla='ds',
       rich_tooltip=True,
       show_legend=True)),
     Slice(slice_name='Genders by State',
       viz_type='dist_bar',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       adhoc_filters=[
      {'clause':'WHERE', 
       'expressionType':'SIMPLE', 
       'filterOptionName':'2745eae5', 
       'comparator':[
        'other'], 
       'operator':'not in', 
       'subject':'state'}],
       viz_type='dist_bar',
       metrics=[
      {'expressionType':'SIMPLE', 
       'column':{'column_name':'sum_boys', 
        'type':'BIGINT(20)'}, 
       'aggregate':'SUM', 
       'label':'Boys', 
       'optionName':'metric_11'},
      {'expressionType':'SIMPLE', 
       'column':{'column_name':'sum_girls', 
        'type':'BIGINT(20)'}, 
       'aggregate':'SUM', 
       'label':'Girls', 
       'optionName':'metric_12'}],
       groupby=[
      'state'])),
     Slice(slice_name='Girls',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       groupby=[
      'name'],
       adhoc_filters=[
      gen_filter('gender', 'girl')],
       row_limit=50,
       timeseries_limit_metric='sum__num')),
     Slice(slice_name='Girl Name Cloud',
       viz_type='word_cloud',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='word_cloud',
       size_from='10',
       series='name',
       size_to='70',
       rotation='square',
       limit='100',
       adhoc_filters=[
      gen_filter('gender', 'girl')])),
     Slice(slice_name='Boys',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       groupby=[
      'name'],
       adhoc_filters=[
      gen_filter('gender', 'boy')],
       row_limit=50)),
     Slice(slice_name='Boy Name Cloud',
       viz_type='word_cloud',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='word_cloud',
       size_from='10',
       series='name',
       size_to='70',
       rotation='square',
       limit='100',
       adhoc_filters=[
      gen_filter('gender', 'boy')])),
     Slice(slice_name='Top 10 Girl Name Share',
       viz_type='area',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       adhoc_filters=[
      gen_filter('gender', 'girl')],
       comparison_type='values',
       groupby=[
      'name'],
       limit=10,
       stacked_style='expand',
       time_grain_sqla='P1D',
       viz_type='area',
       x_axis_forma='smart_date')),
     Slice(slice_name='Top 10 Boy Name Share',
       viz_type='area',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       adhoc_filters=[
      gen_filter('gender', 'boy')],
       comparison_type='values',
       groupby=[
      'name'],
       limit=10,
       stacked_style='expand',
       time_grain_sqla='P1D',
       viz_type='area',
       x_axis_forma='smart_date'))]
    misc_slices = [
     Slice(slice_name='Average and Sum Trends',
       viz_type='dual_line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='dual_line',
       metric={'expressionType':'SIMPLE', 
      'column':{'column_name':'num', 
       'type':'BIGINT(20)'}, 
      'aggregate':'AVG', 
      'label':'AVG(num)', 
      'optionName':'metric_vgops097wej_g8uff99zhk7'},
       metric_2='sum__num',
       granularity_sqla='ds')),
     Slice(slice_name='Num Births Trend',
       viz_type='line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults, viz_type='line')),
     Slice(slice_name='Daily Totals',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       created_by=admin,
       params=get_slice_json(defaults,
       groupby=[
      'ds'],
       since='40 years ago',
       until='now',
       viz_type='table')),
     Slice(slice_name='Number of California Births',
       viz_type='big_number_total',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       metric={'expressionType':'SIMPLE', 
      'column':{'column_name':'num_california', 
       'expression':"CASE WHEN state = 'CA' THEN num ELSE 0 END"}, 
      'aggregate':'SUM', 
      'label':'SUM(num_california)'},
       viz_type='big_number_total',
       granularity_sqla='ds')),
     Slice(slice_name='Top 10 California Names Timeseries',
       viz_type='line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       metrics=[
      {'expressionType':'SIMPLE', 
       'column':{'column_name':'num_california', 
        'expression':"CASE WHEN state = 'CA' THEN num ELSE 0 END"}, 
       'aggregate':'SUM', 
       'label':'SUM(num_california)'}],
       viz_type='line',
       granularity_sqla='ds',
       groupby=[
      'name'],
       timeseries_limit_metric={'expressionType':'SIMPLE', 
      'column':{'column_name':'num_california', 
       'expression':"CASE WHEN state = 'CA' THEN num ELSE 0 END"}, 
      'aggregate':'SUM', 
      'label':'SUM(num_california)'},
       limit='10')),
     Slice(slice_name='Names Sorted by Num in California',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       groupby=[
      'name'],
       row_limit=50,
       timeseries_limit_metric={'expressionType':'SIMPLE', 
      'column':{'column_name':'num_california', 
       'expression':"CASE WHEN state = 'CA' THEN num ELSE 0 END"}, 
      'aggregate':'SUM', 
      'label':'SUM(num_california)'})),
     Slice(slice_name='Number of Girls',
       viz_type='big_number_total',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='big_number_total',
       granularity_sqla='ds',
       adhoc_filters=[
      gen_filter('gender', 'girl')],
       subheader='total female participants')),
     Slice(slice_name='Pivot Table',
       viz_type='pivot_table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='pivot_table', groupby=['name'], columns=['state']))]
    for slc in slices:
        merge_slice(slc)

    for slc in misc_slices:
        merge_slice(slc)
        misc_dash_slices.add(slc.slice_name)

    print('Creating a dashboard')
    dash = db.session.query(Dash).filter_by(slug='births').first()
    if not dash:
        dash = Dash()
        db.session.add(dash)
    dash.published = True
    dash.json_metadata = textwrap.dedent('    {\n        "label_colors": {\n            "Girls": "#FF69B4",\n            "Boys": "#ADD8E6",\n            "girl": "#FF69B4",\n            "boy": "#ADD8E6"\n        }\n    }')
    js = textwrap.dedent('        {\n          "CHART-6GdlekVise": {\n            "children": [],\n            "id": "CHART-6GdlekVise",\n            "meta": {\n              "chartId": 5547,\n              "height": 50,\n              "sliceName": "Top 10 Girl Name Share",\n              "width": 5\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-eh0w37bWbR"\n            ],\n            "type": "CHART"\n          },\n          "CHART-6n9jxb30JG": {\n            "children": [],\n            "id": "CHART-6n9jxb30JG",\n            "meta": {\n              "chartId": 5540,\n              "height": 36,\n              "sliceName": "Genders by State",\n              "width": 5\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW--EyBZQlDi"\n            ],\n            "type": "CHART"\n          },\n          "CHART-Jj9qh1ol-N": {\n            "children": [],\n            "id": "CHART-Jj9qh1ol-N",\n            "meta": {\n              "chartId": 5545,\n              "height": 50,\n              "sliceName": "Boy Name Cloud",\n              "width": 4\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-kzWtcvo8R1"\n            ],\n            "type": "CHART"\n          },\n          "CHART-ODvantb_bF": {\n            "children": [],\n            "id": "CHART-ODvantb_bF",\n            "meta": {\n              "chartId": 5548,\n              "height": 50,\n              "sliceName": "Top 10 Boy Name Share",\n              "width": 5\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-kzWtcvo8R1"\n            ],\n            "type": "CHART"\n          },\n          "CHART-PAXUUqwmX9": {\n            "children": [],\n            "id": "CHART-PAXUUqwmX9",\n            "meta": {\n              "chartId": 5538,\n              "height": 34,\n              "sliceName": "Genders",\n              "width": 3\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-2n0XgiHDgs"\n            ],\n            "type": "CHART"\n          },\n          "CHART-_T6n_K9iQN": {\n            "children": [],\n            "id": "CHART-_T6n_K9iQN",\n            "meta": {\n              "chartId": 5539,\n              "height": 36,\n              "sliceName": "Trends",\n              "width": 7\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW--EyBZQlDi"\n            ],\n            "type": "CHART"\n          },\n          "CHART-eNY0tcE_ic": {\n            "children": [],\n            "id": "CHART-eNY0tcE_ic",\n            "meta": {\n              "chartId": 5537,\n              "height": 34,\n              "sliceName": "Participants",\n              "width": 3\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-2n0XgiHDgs"\n            ],\n            "type": "CHART"\n          },\n          "CHART-g075mMgyYb": {\n            "children": [],\n            "id": "CHART-g075mMgyYb",\n            "meta": {\n              "chartId": 5541,\n              "height": 50,\n              "sliceName": "Girls",\n              "width": 3\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-eh0w37bWbR"\n            ],\n            "type": "CHART"\n          },\n          "CHART-n-zGGE6S1y": {\n            "children": [],\n            "id": "CHART-n-zGGE6S1y",\n            "meta": {\n              "chartId": 5542,\n              "height": 50,\n              "sliceName": "Girl Name Cloud",\n              "width": 4\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-eh0w37bWbR"\n            ],\n            "type": "CHART"\n          },\n          "CHART-vJIPjmcbD3": {\n            "children": [],\n            "id": "CHART-vJIPjmcbD3",\n            "meta": {\n              "chartId": 5543,\n              "height": 50,\n              "sliceName": "Boys",\n              "width": 3\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-kzWtcvo8R1"\n            ],\n            "type": "CHART"\n          },\n          "DASHBOARD_VERSION_KEY": "v2",\n          "GRID_ID": {\n            "children": [\n              "ROW-2n0XgiHDgs",\n              "ROW--EyBZQlDi",\n              "ROW-eh0w37bWbR",\n              "ROW-kzWtcvo8R1"\n            ],\n            "id": "GRID_ID",\n            "parents": [\n              "ROOT_ID"\n            ],\n            "type": "GRID"\n          },\n          "HEADER_ID": {\n            "id": "HEADER_ID",\n            "meta": {\n              "text": "Births"\n            },\n            "type": "HEADER"\n          },\n          "MARKDOWN-zaflB60tbC": {\n            "children": [],\n            "id": "MARKDOWN-zaflB60tbC",\n            "meta": {\n              "code": "<div style=\\"text-align:center\\">  <h1>Birth Names Dashboard</h1>  <img src=\\"/static/assets/images/babies.png\\" style=\\"width:50%;\\"></div>",\n              "height": 34,\n              "width": 6\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID",\n              "ROW-2n0XgiHDgs"\n            ],\n            "type": "MARKDOWN"\n          },\n          "ROOT_ID": {\n            "children": [\n              "GRID_ID"\n            ],\n            "id": "ROOT_ID",\n            "type": "ROOT"\n          },\n          "ROW--EyBZQlDi": {\n            "children": [\n              "CHART-_T6n_K9iQN",\n              "CHART-6n9jxb30JG"\n            ],\n            "id": "ROW--EyBZQlDi",\n            "meta": {\n              "background": "BACKGROUND_TRANSPARENT"\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID"\n            ],\n            "type": "ROW"\n          },\n          "ROW-2n0XgiHDgs": {\n            "children": [\n              "CHART-eNY0tcE_ic",\n              "MARKDOWN-zaflB60tbC",\n              "CHART-PAXUUqwmX9"\n            ],\n            "id": "ROW-2n0XgiHDgs",\n            "meta": {\n              "background": "BACKGROUND_TRANSPARENT"\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID"\n            ],\n            "type": "ROW"\n          },\n          "ROW-eh0w37bWbR": {\n            "children": [\n              "CHART-g075mMgyYb",\n              "CHART-n-zGGE6S1y",\n              "CHART-6GdlekVise"\n            ],\n            "id": "ROW-eh0w37bWbR",\n            "meta": {\n              "background": "BACKGROUND_TRANSPARENT"\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID"\n            ],\n            "type": "ROW"\n          },\n          "ROW-kzWtcvo8R1": {\n            "children": [\n              "CHART-vJIPjmcbD3",\n              "CHART-Jj9qh1ol-N",\n              "CHART-ODvantb_bF"\n            ],\n            "id": "ROW-kzWtcvo8R1",\n            "meta": {\n              "background": "BACKGROUND_TRANSPARENT"\n            },\n            "parents": [\n              "ROOT_ID",\n              "GRID_ID"\n            ],\n            "type": "ROW"\n          }\n        }\n        ')
    pos = json.loads(js)
    dash.slices = [slc for slc in slices if slc.viz_type != 'markup']
    update_slice_ids(pos, dash.slices)
    dash.dashboard_title = 'USA Births Names'
    dash.position_json = json.dumps(pos, indent=4)
    dash.slug = 'births'
    db.session.commit()