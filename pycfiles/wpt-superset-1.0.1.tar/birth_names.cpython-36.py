# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leonardo/proyectos/dashboard/incubator-superset/superset/data/birth_names.py
# Compiled at: 2019-01-19 16:19:59
# Size of source mod 2**32: 18557 bytes
import gzip, json, os, textwrap, pandas as pd
from sqlalchemy import DateTime, String
from superset import db, security_manager
from superset.connectors.sqla.models import SqlMetric, TableColumn
from superset.utils.core import get_or_create_main_db
from .helpers import config, Dash, DATA_FOLDER, get_slice_json, merge_slice, Slice, TBL, update_slice_ids

def load_birth_names():
    """Loading birth name dataset from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, 'birth_names.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime((pdf.ds), unit='ms')
    pdf.to_sql('birth_names',
      (db.engine),
      if_exists='replace',
      chunksize=500,
      dtype={'ds':DateTime, 
     'gender':String(16), 
     'state':String(10), 
     'name':String(255)},
      index=False)
    print('Done loading table!')
    print('-' * 80)
    print('Creating table [birth_names] reference')
    obj = db.session.query(TBL).filter_by(table_name='birth_names').first()
    if not obj:
        obj = TBL(table_name='birth_names')
    obj.main_dttm_col = 'ds'
    obj.database = get_or_create_main_db()
    obj.filter_select_enabled = True
    if not any(col.column_name == 'num_california' for col in obj.columns):
        obj.columns.append(TableColumn(column_name='num_california',
          expression="CASE WHEN state = 'CA' THEN num ELSE 0 END"))
    if not any(col.metric_name == 'sum__num' for col in obj.metrics):
        obj.metrics.append(SqlMetric(metric_name='sum__num',
          expression='SUM(num)'))
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    defaults = {'compare_lag':'10', 
     'compare_suffix':'o10Y', 
     'limit':'25', 
     'granularity_sqla':'ds', 
     'groupby':[],  'metric':'sum__num', 
     'metrics':[
      'sum__num'], 
     'row_limit':config.get('ROW_LIMIT'), 
     'since':'100 years ago', 
     'until':'now', 
     'viz_type':'table', 
     'where':'', 
     'markup_type':'markdown'}
    admin = security_manager.find_user('admin')
    print('Creating some slices')
    slices = [
     Slice(slice_name='Girls',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       groupby=[
      'name'],
       filters=[
      {'col':'gender', 
       'op':'in', 
       'val':[
        'girl']}],
       row_limit=50,
       timeseries_limit_metric='sum__num')),
     Slice(slice_name='Boys',
       viz_type='table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       groupby=[
      'name'],
       filters=[
      {'col':'gender', 
       'op':'in', 
       'val':[
        'boy']}],
       row_limit=50)),
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
       params=get_slice_json(defaults,
       viz_type='pie',
       groupby=['gender'])),
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
     Slice(slice_name='Trends',
       viz_type='line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='line',
       groupby=['name'],
       granularity_sqla='ds',
       rich_tooltip=True,
       show_legend=True)),
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
     Slice(slice_name='Title',
       viz_type='markup',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='markup',
       markup_type='html',
       code="    <div style='text-align:center'>\n        <h1>Birth Names Dashboard</h1>\n        <p>\n            The source dataset came from\n            <a href='https://github.com/hadley/babynames' target='_blank'>[here]</a>\n        </p>\n        <img src='/static/assets/images/babytux.jpg'>\n    </div>\n    ")),
     Slice(slice_name='Name Cloud',
       viz_type='word_cloud',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='word_cloud',
       size_from='10',
       series='name',
       size_to='70',
       rotation='square',
       limit='100')),
     Slice(slice_name='Pivot Table',
       viz_type='pivot_table',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='pivot_table',
       metrics=['sum__num'],
       groupby=[
      'name'],
       columns=['state'])),
     Slice(slice_name='Number of Girls',
       viz_type='big_number_total',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='big_number_total',
       granularity_sqla='ds',
       filters=[
      {'col':'gender', 
       'op':'in', 
       'val':[
        'girl']}],
       subheader='total female participants')),
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
     Slice(slice_name='Num Births Trend',
       viz_type='line',
       datasource_type='table',
       datasource_id=(tbl.id),
       params=get_slice_json(defaults,
       viz_type='line')),
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
       viz_type='table'))]
    for slc in slices:
        merge_slice(slc)

    print('Creating a dashboard')
    dash = db.session.query(Dash).filter_by(dashboard_title='Births').first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent('{\n    "CHART-0dd270f0": {\n        "meta": {\n            "chartId": 51,\n            "width": 2,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-0dd270f0",\n        "children": []\n    },\n    "CHART-a3c21bcc": {\n        "meta": {\n            "chartId": 52,\n            "width": 2,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-a3c21bcc",\n        "children": []\n    },\n    "CHART-976960a5": {\n        "meta": {\n            "chartId": 53,\n            "width": 2,\n            "height": 25\n        },\n        "type": "CHART",\n        "id": "CHART-976960a5",\n        "children": []\n    },\n    "CHART-58575537": {\n        "meta": {\n            "chartId": 54,\n            "width": 2,\n            "height": 25\n        },\n        "type": "CHART",\n        "id": "CHART-58575537",\n        "children": []\n    },\n    "CHART-e9cd8f0b": {\n        "meta": {\n            "chartId": 55,\n            "width": 8,\n            "height": 38\n        },\n        "type": "CHART",\n        "id": "CHART-e9cd8f0b",\n        "children": []\n    },\n    "CHART-e440d205": {\n        "meta": {\n            "chartId": 56,\n            "width": 8,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-e440d205",\n        "children": []\n    },\n    "CHART-59444e0b": {\n        "meta": {\n            "chartId": 57,\n            "width": 3,\n            "height": 38\n        },\n        "type": "CHART",\n        "id": "CHART-59444e0b",\n        "children": []\n    },\n    "CHART-e2cb4997": {\n        "meta": {\n            "chartId": 59,\n            "width": 4,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-e2cb4997",\n        "children": []\n    },\n    "CHART-e8774b49": {\n        "meta": {\n            "chartId": 60,\n            "width": 12,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-e8774b49",\n        "children": []\n    },\n    "CHART-985bfd1e": {\n        "meta": {\n            "chartId": 61,\n            "width": 4,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-985bfd1e",\n        "children": []\n    },\n    "CHART-17f13246": {\n        "meta": {\n            "chartId": 62,\n            "width": 4,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-17f13246",\n        "children": []\n    },\n    "CHART-729324f6": {\n        "meta": {\n            "chartId": 63,\n            "width": 4,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-729324f6",\n        "children": []\n    },\n    "COLUMN-25a865d6": {\n        "meta": {\n            "width": 4,\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "COLUMN",\n        "id": "COLUMN-25a865d6",\n        "children": [\n            "ROW-cc97c6ac",\n            "CHART-e2cb4997"\n        ]\n    },\n    "COLUMN-4557b6ba": {\n        "meta": {\n            "width": 8,\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "COLUMN",\n        "id": "COLUMN-4557b6ba",\n        "children": [\n            "ROW-d2e78e59",\n            "CHART-e9cd8f0b"\n        ]\n    },\n    "GRID_ID": {\n        "type": "GRID",\n        "id": "GRID_ID",\n        "children": [\n            "ROW-8515ace3",\n            "ROW-1890385f",\n            "ROW-f0b64094",\n            "ROW-be9526b8"\n        ]\n    },\n    "HEADER_ID": {\n        "meta": {\n            "text": "Births"\n        },\n        "type": "HEADER",\n        "id": "HEADER_ID"\n    },\n    "MARKDOWN-00178c27": {\n        "meta": {\n            "width": 5,\n            "code": "<div style=\\"text-align:center\\">\\n <h1>Birth Names Dashboard</h1>\\n <p>\\n The source dataset came from\\n <a href=\\"https://github.com/hadley/babynames\\" target=\\"_blank\\">[here]</a>\\n </p>\\n <img src=\\"/static/assets/images/babytux.jpg\\">\\n</div>\\n",\n            "height": 38\n        },\n        "type": "MARKDOWN",\n        "id": "MARKDOWN-00178c27",\n        "children": []\n    },\n    "ROOT_ID": {\n        "type": "ROOT",\n        "id": "ROOT_ID",\n        "children": [\n            "GRID_ID"\n        ]\n    },\n    "ROW-1890385f": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-1890385f",\n        "children": [\n            "CHART-e440d205",\n            "CHART-0dd270f0",\n            "CHART-a3c21bcc"\n        ]\n    },\n    "ROW-8515ace3": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-8515ace3",\n        "children": [\n            "COLUMN-25a865d6",\n            "COLUMN-4557b6ba"\n        ]\n    },\n    "ROW-be9526b8": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-be9526b8",\n        "children": [\n            "CHART-985bfd1e",\n            "CHART-17f13246",\n            "CHART-729324f6"\n        ]\n    },\n    "ROW-cc97c6ac": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-cc97c6ac",\n        "children": [\n            "CHART-976960a5",\n            "CHART-58575537"\n        ]\n    },\n    "ROW-d2e78e59": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-d2e78e59",\n        "children": [\n            "MARKDOWN-00178c27",\n            "CHART-59444e0b"\n        ]\n    },\n    "ROW-f0b64094": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-f0b64094",\n        "children": [\n            "CHART-e8774b49"\n        ]\n    },\n    "DASHBOARD_VERSION_KEY": "v2"\n}\n        ')
    pos = json.loads(js)
    dash.slices = [slc for slc in slices if slc.viz_type != 'markup']
    update_slice_ids(pos, dash.slices)
    dash.dashboard_title = 'Births'
    dash.position_json = json.dumps(pos, indent=4)
    dash.slug = 'births'
    db.session.merge(dash)
    db.session.commit()