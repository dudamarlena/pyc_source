# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /u01/github/rdc-hand-china/superset/superset/data/__init__.py
# Compiled at: 2016-11-30 01:04:13
# Size of source mod 2**32: 33840 bytes
"""Loads datasets, dashboards and slices in a new superset instance"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import gzip, json, os, textwrap, datetime, random, pandas as pd
from sqlalchemy import String, DateTime, Date, Float, BigInteger
from superset import app, db, models, utils
from superset.security import get_or_create_main_db
DB = models.Database
Slice = models.Slice
TBL = models.SqlaTable
Dash = models.Dashboard
config = app.config
DATA_FOLDER = os.path.join(config.get('BASE_DIR'), 'data')
misc_dash_slices = []

def merge_slice(slc):
    o = db.session.query(Slice).filter_by(slice_name=slc.slice_name).first()
    if o:
        db.session.delete(o)
    db.session.add(slc)
    db.session.commit()


def get_slice_json(defaults, **kwargs):
    d = defaults.copy()
    d.update(kwargs)
    return json.dumps(d, indent=4, sort_keys=True)


def load_energy():
    """Loads an energy related dataset to use with sankey and graphs"""
    tbl_name = 'energy_usage'
    with gzip.open(os.path.join(DATA_FOLDER, 'energy.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.to_sql(tbl_name, db.engine, if_exists='replace', chunksize=500, dtype={'source': String(255), 
     'target': String(255), 
     'value': Float()}, index=False)
    print('Creating table [wb_health_population] reference')
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = 'Energy consumption'
    tbl.is_featured = True
    tbl.database = get_or_create_main_db()
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    slc = Slice(slice_name='Energy Sankey', viz_type='sankey', datasource_type='table', datasource_id=tbl.id, params=textwrap.dedent('        {\n            "collapsed_fieldsets": "",\n            "datasource_id": "3",\n            "datasource_name": "energy_usage",\n            "datasource_type": "table",\n            "flt_col_0": "source",\n            "flt_eq_0": "",\n            "flt_op_0": "in",\n            "groupby": [\n                "source",\n                "target"\n            ],\n            "having": "",\n            "metric": "sum__value",\n            "row_limit": "5000",\n            "slice_name": "Energy Sankey",\n            "viz_type": "sankey",\n            "where": ""\n        }\n        '))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)
    slc = Slice(slice_name='Energy Force Layout', viz_type='directed_force', datasource_type='table', datasource_id=tbl.id, params=textwrap.dedent('        {\n            "charge": "-500",\n            "collapsed_fieldsets": "",\n            "datasource_id": "1",\n            "datasource_name": "energy_usage",\n            "datasource_type": "table",\n            "flt_col_0": "source",\n            "flt_eq_0": "",\n            "flt_op_0": "in",\n            "groupby": [\n                "source",\n                "target"\n            ],\n            "having": "",\n            "link_length": "200",\n            "metric": "sum__value",\n            "row_limit": "5000",\n            "slice_name": "Force",\n            "viz_type": "directed_force",\n            "where": ""\n        }\n        '))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)
    slc = Slice(slice_name='Heatmap', viz_type='heatmap', datasource_type='table', datasource_id=tbl.id, params=textwrap.dedent('        {\n            "all_columns_x": "source",\n            "all_columns_y": "target",\n            "canvas_image_rendering": "pixelated",\n            "collapsed_fieldsets": "",\n            "datasource_id": "1",\n            "datasource_name": "energy_usage",\n            "datasource_type": "table",\n            "flt_col_0": "source",\n            "flt_eq_0": "",\n            "flt_op_0": "in",\n            "having": "",\n            "linear_color_scheme": "blue_white_yellow",\n            "metric": "sum__value",\n            "normalize_across": "heatmap",\n            "slice_name": "Heatmap",\n            "viz_type": "heatmap",\n            "where": "",\n            "xscale_interval": "1",\n            "yscale_interval": "1"\n        }\n        '))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)


def load_world_bank_health_n_pop():
    """Loads the world bank health dataset, slices and a dashboard"""
    tbl_name = 'wb_health_population'
    with gzip.open(os.path.join(DATA_FOLDER, 'countries.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.columns = [col.replace('.', '_') for col in pdf.columns]
    pdf.year = pd.to_datetime(pdf.year)
    pdf.to_sql(tbl_name, db.engine, if_exists='replace', chunksize=50, dtype={'year': DateTime(), 
     'country_code': String(3), 
     'country_name': String(255), 
     'region': String(255)}, index=False)
    print('Creating table [wb_health_population] reference')
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = utils.readfile(os.path.join(DATA_FOLDER, 'countries.md'))
    tbl.main_dttm_col = 'year'
    tbl.is_featured = True
    tbl.database = get_or_create_main_db()
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    defaults = {'compare_lag': '10', 
     'compare_suffix': 'o10Y', 
     'datasource_id': '1', 
     'datasource_name': 'birth_names', 
     'datasource_type': 'table', 
     'limit': '25', 
     'granularity': 'year', 
     'groupby': [], 
     'metric': 'sum__SP_POP_TOTL', 
     'metrics': ['sum__SP_POP_TOTL'], 
     'row_limit': config.get('ROW_LIMIT'), 
     'since': '2014-01-01', 
     'until': '2014-01-02', 
     'where': '', 
     'markup_type': 'markdown', 
     'country_fieldtype': 'cca3', 
     'secondary_metric': 'sum__SP_POP_TOTL', 
     'entity': 'country_code', 
     'show_bubbles': 'y'}
    print('Creating slices')
    slices = [
     Slice(slice_name='Region Filter', viz_type='filter_box', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='filter_box', groupby=[
      'region', 'country_name'])),
     Slice(slice_name="World's Population", viz_type='big_number', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, since='2000', viz_type='big_number', compare_lag='10', metric='sum__SP_POP_TOTL', compare_suffix='over 10Y')),
     Slice(slice_name='Most Populated Countries', viz_type='table', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='table', metrics=[
      'sum__SP_POP_TOTL'], groupby=[
      'country_name'])),
     Slice(slice_name='Growth Rate', viz_type='line', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='line', since='1960-01-01', metrics=[
      'sum__SP_POP_TOTL'], num_period_compare='10', groupby=[
      'country_name'])),
     Slice(slice_name='% Rural', viz_type='world_map', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='world_map', metric='sum__SP_RUR_TOTL_ZS', num_period_compare='10')),
     Slice(slice_name='Life Expectancy VS Rural %', viz_type='bubble', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='bubble', since='2011-01-01', until='2011-01-02', series='region', limit='0', entity='country_name', x='sum__SP_RUR_TOTL_ZS', y='sum__SP_DYN_LE00_IN', size='sum__SP_POP_TOTL', max_bubble_size='50', flt_col_1='country_code', flt_op_1='not in', flt_eq_1='TCA,MNP,DMA,MHL,MCO,SXM,CYM,TUV,IMY,KNA,ASM,ADO,AMA,PLW', num_period_compare='10')),
     Slice(slice_name='Rural Breakdown', viz_type='sunburst', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='sunburst', groupby=[
      'region', 'country_name'], secondary_metric='sum__SP_RUR_TOTL', since='2011-01-01', until='2011-01-01')),
     Slice(slice_name="World's Pop Growth", viz_type='area', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, since='1960-01-01', until='now', viz_type='area', groupby=[
      'region'])),
     Slice(slice_name='Box plot', viz_type='box_plot', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, since='1960-01-01', until='now', whisker_options='Min/max (no outliers)', viz_type='box_plot', groupby=[
      'region'])),
     Slice(slice_name='Treemap', viz_type='treemap', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, since='1960-01-01', until='now', viz_type='treemap', metrics=[
      'sum__SP_POP_TOTL'], groupby=[
      'region', 'country_code'])),
     Slice(slice_name='Parallel Coordinates', viz_type='para', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, since='2011-01-01', until='2011-01-01', viz_type='para', limit=100, metrics=[
      'sum__SP_POP_TOTL',
      'sum__SP_RUR_TOTL_ZS',
      'sum__SH_DYN_AIDS'], secondary_metric='sum__SP_POP_TOTL', series='country_name'))]
    misc_dash_slices.append(slices[(-1)].slice_name)
    for slc in slices:
        merge_slice(slc)

    print("Creating a World's Health Bank dashboard")
    dash_name = "World's Bank Data"
    slug = 'world_health'
    dash = db.session.query(Dash).filter_by(slug=slug).first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent('    [\n        {\n            "col": 1,\n            "row": 0,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1231"\n        },\n        {\n            "col": 1,\n            "row": 2,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1232"\n        },\n        {\n            "col": 10,\n            "row": 0,\n            "size_x": 3,\n            "size_y": 7,\n            "slice_id": "1233"\n        },\n        {\n            "col": 1,\n            "row": 4,\n            "size_x": 6,\n            "size_y": 3,\n            "slice_id": "1234"\n        },\n        {\n            "col": 3,\n            "row": 0,\n            "size_x": 7,\n            "size_y": 4,\n            "slice_id": "1235"\n        },\n        {\n            "col": 5,\n            "row": 7,\n            "size_x": 8,\n            "size_y": 4,\n            "slice_id": "1236"\n        },\n        {\n            "col": 7,\n            "row": 4,\n            "size_x": 3,\n            "size_y": 3,\n            "slice_id": "1237"\n        },\n        {\n            "col": 1,\n            "row": 7,\n            "size_x": 4,\n            "size_y": 4,\n            "slice_id": "1238"\n        },\n        {\n            "col": 9,\n            "row": 11,\n            "size_x": 4,\n            "size_y": 4,\n            "slice_id": "1239"\n        },\n        {\n            "col": 1,\n            "row": 11,\n            "size_x": 8,\n            "size_y": 4,\n            "slice_id": "1240"\n        }\n    ]\n    ')
    l = json.loads(js)
    for i, pos in enumerate(l):
        pos['slice_id'] = str(slices[i].id)

    dash.dashboard_title = dash_name
    dash.position_json = json.dumps(l, indent=4)
    dash.slug = slug
    dash.slices = slices[:-1]
    db.session.merge(dash)
    db.session.commit()


def load_css_templates():
    """Loads 2 css templates to demonstrate the feature"""
    print('Creating default CSS templates')
    CSS = models.CssTemplate
    obj = db.session.query(CSS).filter_by(template_name='Flat').first()
    if not obj:
        obj = CSS(template_name='Flat')
    css = textwrap.dedent("    .gridster div.widget {\n        transition: background-color 0.5s ease;\n        background-color: #FAFAFA;\n        border: 1px solid #CCC;\n        box-shadow: none;\n        border-radius: 0px;\n    }\n    .gridster div.widget:hover {\n        border: 1px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .chart-header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
    obj = db.session.query(CSS).filter_by(template_name='Courier Black').first()
    if not obj:
        obj = CSS(template_name='Courier Black')
    css = textwrap.dedent("    .gridster div.widget {\n        transition: background-color 0.5s ease;\n        background-color: #EEE;\n        border: 2px solid #444;\n        border-radius: 15px;\n        box-shadow: none;\n    }\n    h2 {\n        color: white;\n        font-size: 52px;\n    }\n    .navbar {\n        box-shadow: none;\n    }\n    .gridster div.widget:hover {\n        border: 2px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .chart-header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    .nvd3 text {\n        font-size: 12px;\n        font-family: inherit;\n    }\n    body{\n        background: #000;\n        font-family: Courier, Monaco, monospace;;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()


def load_birth_names():
    """Loading birth name dataset from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, 'birth_names.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit='ms')
    pdf.to_sql('birth_names', db.engine, if_exists='replace', chunksize=500, dtype={'ds': DateTime, 
     'gender': String(16), 
     'state': String(10), 
     'name': String(255)}, index=False)
    l = []
    print('Done loading table!')
    print('-' * 80)
    print('Creating table [birth_names] reference')
    obj = db.session.query(TBL).filter_by(table_name='birth_names').first()
    if not obj:
        obj = TBL(table_name='birth_names')
    obj.main_dttm_col = 'ds'
    obj.database = get_or_create_main_db()
    obj.is_featured = True
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    defaults = {'compare_lag': '10', 
     'compare_suffix': 'o10Y', 
     'datasource_id': '1', 
     'datasource_name': 'birth_names', 
     'datasource_type': 'table', 
     'flt_op_1': 'in', 
     'limit': '25', 
     'granularity': 'ds', 
     'groupby': [], 
     'metric': 'sum__num', 
     'metrics': ['sum__num'], 
     'row_limit': config.get('ROW_LIMIT'), 
     'since': '100 years ago', 
     'until': 'now', 
     'viz_type': 'table', 
     'where': '', 
     'markup_type': 'markdown'}
    print('Creating some slices')
    slices = [
     Slice(slice_name='Girls', viz_type='table', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, groupby=[
      'name'], flt_col_1='gender', flt_eq_1='girl', row_limit=50)),
     Slice(slice_name='Boys', viz_type='table', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, groupby=[
      'name'], flt_col_1='gender', flt_eq_1='boy', row_limit=50)),
     Slice(slice_name='Participants', viz_type='big_number', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='big_number', granularity='ds', compare_lag='5', compare_suffix='over 5Y')),
     Slice(slice_name='Genders', viz_type='pie', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='pie', groupby=['gender'])),
     Slice(slice_name='Genders by State', viz_type='dist_bar', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, flt_eq_1='other', viz_type='dist_bar', metrics=[
      'sum__sum_girls', 'sum__sum_boys'], groupby=[
      'state'], flt_op_1='not in', flt_col_1='state')),
     Slice(slice_name='Trends', viz_type='line', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='line', groupby=['name'], granularity='ds', rich_tooltip='y', show_legend='y')),
     Slice(slice_name='Title', viz_type='markup', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='markup', markup_type='html', code='<div style="text-align:center">\n    <h1>Birth Names Dashboard</h1>\n    <p>\n        The source dataset came from\n        <a href="https://github.com/hadley/babynames">[here]</a>\n    </p>\n    <img src="/static/assets/images/babytux.jpg">\n</div>\n')),
     Slice(slice_name='Name Cloud', viz_type='word_cloud', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='word_cloud', size_from='10', series='name', size_to='70', rotation='square', limit='100')),
     Slice(slice_name='Pivot Table', viz_type='pivot_table', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='pivot_table', metrics=['sum__num'], groupby=[
      'name'], columns=['state'])),
     Slice(slice_name='Number of Girls', viz_type='big_number_total', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type='big_number_total', granularity='ds', flt_col_1='gender', flt_eq_1='girl', subheader='total female participants'))]
    for slc in slices:
        merge_slice(slc)

    print('Creating a dashboard')
    dash = db.session.query(Dash).filter_by(dashboard_title='Births').first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent('    [\n        {\n            "col": 9,\n            "row": 6,\n            "size_x": 2,\n            "size_y": 4,\n            "slice_id": "1267"\n        },\n        {\n            "col": 11,\n            "row": 6,\n            "size_x": 2,\n            "size_y": 4,\n            "slice_id": "1268"\n        },\n        {\n            "col": 1,\n            "row": 0,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1269"\n        },\n        {\n            "col": 3,\n            "row": 0,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1270"\n        },\n        {\n            "col": 5,\n            "row": 3,\n            "size_x": 8,\n            "size_y": 3,\n            "slice_id": "1271"\n        },\n        {\n            "col": 1,\n            "row": 6,\n            "size_x": 8,\n            "size_y": 4,\n            "slice_id": "1272"\n        },\n        {\n            "col": 10,\n            "row": 0,\n            "size_x": 3,\n            "size_y": 3,\n            "slice_id": "1273"\n        },\n        {\n            "col": 5,\n            "row": 0,\n            "size_x": 5,\n            "size_y": 3,\n            "slice_id": "1274"\n        },\n        {\n            "col": 1,\n            "row": 2,\n            "size_x": 4,\n            "size_y": 4,\n            "slice_id": "1275"\n        }\n    ]\n        ')
    l = json.loads(js)
    for i, pos in enumerate(l):
        pos['slice_id'] = str(slices[i].id)

    dash.dashboard_title = 'Births'
    dash.position_json = json.dumps(l, indent=4)
    dash.slug = 'births'
    dash.slices = slices[:-1]
    db.session.merge(dash)
    db.session.commit()


def load_unicode_test_data():
    """Loading unicode test dataset from a csv file in the repo"""
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'unicode_utf8_unixnl_test.csv'), encoding='utf-8')
    df['date'] = datetime.datetime.now().date()
    df['value'] = [random.randint(1, 100) for _ in range(len(df))]
    df.to_sql('unicode_test', db.engine, if_exists='replace', chunksize=500, dtype={'phrase': String(500), 
     'short_phrase': String(10), 
     'with_missing': String(100), 
     'date': Date(), 
     'value': Float()}, index=False)
    print('Done loading table!')
    print('-' * 80)
    print('Creating table [unicode_test] reference')
    obj = db.session.query(TBL).filter_by(table_name='unicode_test').first()
    if not obj:
        obj = TBL(table_name='unicode_test')
    obj.main_dttm_col = 'date'
    obj.database = get_or_create_main_db()
    obj.is_featured = False
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {'datasource_id': '3', 
     'datasource_name': 'unicode_test', 
     'datasource_type': 'table', 
     'flt_op_1': 'in', 
     'granularity': 'date', 
     'groupby': [], 
     'metric': 'sum__value', 
     'row_limit': config.get('ROW_LIMIT'), 
     'since': '100 years ago', 
     'until': 'now', 
     'where': '', 
     'viz_type': 'word_cloud', 
     'size_from': '10', 
     'series': 'short_phrase', 
     'size_to': '70', 
     'rotation': 'square', 
     'limit': '100'}
    print('Creating a slice')
    slc = Slice(slice_name='Unicode Cloud', viz_type='word_cloud', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(slice_data))
    merge_slice(slc)
    print('Creating a dashboard')
    dash = db.session.query(Dash).filter_by(dashboard_title='Unicode Test').first()
    if not dash:
        dash = Dash()
    pos = {'size_y': 4, 
     'size_x': 4, 
     'col': 1, 
     'row': 1, 
     'slice_id': slc.id}
    dash.dashboard_title = 'Unicode Test'
    dash.position_json = json.dumps([pos], indent=4)
    dash.slug = 'unicode-test'
    dash.slices = [slc]
    db.session.merge(dash)
    db.session.commit()


def load_random_time_series_data():
    """Loading random time series data from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, 'random_time_series.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit='s')
    pdf.to_sql('random_time_series', db.engine, if_exists='replace', chunksize=500, dtype={'ds': DateTime}, index=False)
    print('Done loading table!')
    print('-' * 80)
    print('Creating table [random_time_series] reference')
    obj = db.session.query(TBL).filter_by(table_name='random_time_series').first()
    if not obj:
        obj = TBL(table_name='random_time_series')
    obj.main_dttm_col = 'ds'
    obj.database = get_or_create_main_db()
    obj.is_featured = False
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {'datasource_id': '6', 
     'datasource_name': 'random_time_series', 
     'datasource_type': 'table', 
     'granularity': 'day', 
     'row_limit': config.get('ROW_LIMIT'), 
     'since': '1 year ago', 
     'until': 'now', 
     'where': '', 
     'viz_type': 'cal_heatmap', 
     'domain_granularity': 'month', 
     'subdomain_granularity': 'day'}
    print('Creating a slice')
    slc = Slice(slice_name='Calendar Heatmap', viz_type='cal_heatmap', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(slice_data))
    merge_slice(slc)


def load_long_lat_data():
    """Loading lat/long data from a csv file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, 'san_francisco.csv.gz')) as (f):
        pdf = pd.read_csv(f, encoding='utf-8')
    pdf['date'] = datetime.datetime.now().date()
    pdf['occupancy'] = [random.randint(1, 6) for _ in range(len(pdf))]
    pdf['radius_miles'] = [random.uniform(1, 3) for _ in range(len(pdf))]
    pdf.to_sql('long_lat', db.engine, if_exists='replace', chunksize=500, dtype={'longitude': Float(), 
     'latitude': Float(), 
     'number': Float(), 
     'street': String(100), 
     'unit': String(10), 
     'city': String(50), 
     'district': String(50), 
     'region': String(50), 
     'postcode': Float(), 
     'id': String(100), 
     'date': Date(), 
     'occupancy': Float(), 
     'radius_miles': Float()}, index=False)
    print('Done loading table!')
    print('-' * 80)
    print('Creating table reference')
    obj = db.session.query(TBL).filter_by(table_name='long_lat').first()
    if not obj:
        obj = TBL(table_name='long_lat')
    obj.main_dttm_col = 'date'
    obj.database = get_or_create_main_db()
    obj.is_featured = False
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {'datasource_id': '7', 
     'datasource_name': 'long_lat', 
     'datasource_type': 'table', 
     'granularity': 'day', 
     'since': '2014-01-01', 
     'until': '2016-12-12', 
     'where': '', 
     'viz_type': 'mapbox', 
     'all_columns_x': 'LON', 
     'all_columns_y': 'LAT', 
     'mapbox_style': 'mapbox://styles/mapbox/light-v9', 
     'all_columns': ['occupancy'], 
     'row_limit': 500000}
    print('Creating a slice')
    slc = Slice(slice_name='Mapbox Long/Lat', viz_type='mapbox', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(slice_data))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)


def load_multiformat_time_series_data():
    """Loading time series data from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, 'multiformat_time_series.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit='s')
    pdf.ds2 = pd.to_datetime(pdf.ds2, unit='s')
    pdf.to_sql('multiformat_time_series', db.engine, if_exists='replace', chunksize=500, dtype={'ds': Date, 
     'ds2': DateTime, 
     'epoch_s': BigInteger, 
     'epoch_ms': BigInteger, 
     'string0': String(100), 
     'string1': String(100), 
     'string2': String(100), 
     'string3': String(100)}, index=False)
    print('Done loading table!')
    print('-' * 80)
    print('Creating table [multiformat_time_series] reference')
    obj = db.session.query(TBL).filter_by(table_name='multiformat_time_series').first()
    if not obj:
        obj = TBL(table_name='multiformat_time_series')
    obj.main_dttm_col = 'ds'
    obj.database = get_or_create_main_db()
    obj.is_featured = False
    dttm_and_expr_dict = {'ds': [None, None], 
     'ds2': [None, None], 
     'epoch_s': ['epoch_s', None], 
     'epoch_ms': ['epoch_ms', None], 
     'string2': ['%Y%m%d-%H%M%S', None], 
     'string1': ['%Y-%m-%d^%H:%M:%S', None], 
     'string0': ['%Y-%m-%d %H:%M:%S.%f', None], 
     'string3': ['%Y/%m/%d%H:%M:%S.%f', None]}
    for col in obj.columns:
        dttm_and_expr = dttm_and_expr_dict[col.column_name]
        col.python_date_format = dttm_and_expr[0]
        col.dbatabase_expr = dttm_and_expr[1]
        col.is_dttm = True

    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    print('Creating some slices')
    for i, col in enumerate(tbl.columns):
        slice_data = {'granularity_sqla': col.column_name, 
         'datasource_id': '8', 
         'datasource_name': 'multiformat_time_series', 
         'datasource_type': 'table', 
         'granularity': 'day', 
         'row_limit': config.get('ROW_LIMIT'), 
         'since': '1 year ago', 
         'until': 'now', 
         'where': '', 
         'viz_type': 'cal_heatmap', 
         'domain_granularity': 'month', 
         'subdomain_granularity': 'day'}
        slc = Slice(slice_name='Calendar Heatmap multiformat ' + str(i), viz_type='cal_heatmap', datasource_type='table', datasource_id=tbl.id, params=get_slice_json(slice_data))
        merge_slice(slc)

    misc_dash_slices.append(slc.slice_name)


def load_misc_dashboard():
    """Loading a dasbhoard featuring misc charts"""
    print('Creating the dashboard')
    db.session.expunge_all()
    DASH_SLUG = 'misc_charts'
    dash = db.session.query(Dash).filter_by(slug=DASH_SLUG).first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent('    [\n        {\n            "col": 1,\n            "row": 7,\n            "size_x": 6,\n            "size_y": 4,\n            "slice_id": "442"\n        },\n        {\n            "col": 1,\n            "row": 2,\n            "size_x": 6,\n            "size_y": 5,\n            "slice_id": "443"\n        },\n        {\n            "col": 7,\n            "row": 2,\n            "size_x": 6,\n            "size_y": 4,\n            "slice_id": "444"\n        },\n        {\n            "col": 9,\n            "row": 0,\n            "size_x": 4,\n            "size_y": 2,\n            "slice_id": "455"\n        },\n        {\n            "col": 7,\n            "row": 6,\n            "size_x": 6,\n            "size_y": 5,\n            "slice_id": "467"\n        },\n        {\n            "col": 1,\n            "row": 0,\n            "size_x": 8,\n            "size_y": 2,\n            "slice_id": "475"\n        }\n    ]\n    ')
    l = json.loads(js)
    slices = db.session.query(Slice).filter(Slice.slice_name.in_(misc_dash_slices)).all()
    slices = sorted(slices, key=lambda x: x.id)
    for i, pos in enumerate(l):
        pos['slice_id'] = str(slices[i].id)

    dash.dashboard_title = 'Misc Charts'
    dash.position_json = json.dumps(l, indent=4)
    dash.slug = DASH_SLUG
    dash.slices = slices
    db.session.merge(dash)
    db.session.commit()