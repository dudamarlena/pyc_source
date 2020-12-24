# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/liudong/caravel/caravel/data/__init__.py
# Compiled at: 2016-10-11 03:34:44
__doc__ = b'Loads datasets, dashboards and slices in a new caravel instance'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import gzip, json, os, textwrap, datetime, random, pandas as pd
from sqlalchemy import String, DateTime, Date, Float, BigInteger
import caravel
from caravel import app, db, models, utils
DB = models.Database
Slice = models.Slice
TBL = models.SqlaTable
Dash = models.Dashboard
config = app.config
DATA_FOLDER = os.path.join(config.get(b'BASE_DIR'), b'data')
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
    tbl_name = b'energy_usage'
    with gzip.open(os.path.join(DATA_FOLDER, b'energy.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.to_sql(tbl_name, db.engine, if_exists=b'replace', chunksize=500, dtype={b'source': String(255), 
       b'target': String(255), 
       b'value': Float()}, index=False)
    print(b'Creating table [wb_health_population] reference')
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = b'Energy consumption'
    tbl.is_featured = True
    tbl.database = utils.get_or_create_main_db(caravel)
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    slc = Slice(slice_name=b'Energy Sankey', viz_type=b'sankey', datasource_type=b'table', datasource_id=tbl.id, params=textwrap.dedent(b'        {\n            "collapsed_fieldsets": "",\n            "datasource_id": "3",\n            "datasource_name": "energy_usage",\n            "datasource_type": "table",\n            "flt_col_0": "source",\n            "flt_eq_0": "",\n            "flt_op_0": "in",\n            "groupby": [\n                "source",\n                "target"\n            ],\n            "having": "",\n            "metric": "sum__value",\n            "row_limit": "5000",\n            "slice_name": "Energy Sankey",\n            "viz_type": "sankey",\n            "where": ""\n        }\n        '))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)
    slc = Slice(slice_name=b'Energy Force Layout', viz_type=b'directed_force', datasource_type=b'table', datasource_id=tbl.id, params=textwrap.dedent(b'        {\n            "charge": "-500",\n            "collapsed_fieldsets": "",\n            "datasource_id": "1",\n            "datasource_name": "energy_usage",\n            "datasource_type": "table",\n            "flt_col_0": "source",\n            "flt_eq_0": "",\n            "flt_op_0": "in",\n            "groupby": [\n                "source",\n                "target"\n            ],\n            "having": "",\n            "link_length": "200",\n            "metric": "sum__value",\n            "row_limit": "5000",\n            "slice_name": "Force",\n            "viz_type": "directed_force",\n            "where": ""\n        }\n        '))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)
    slc = Slice(slice_name=b'Heatmap', viz_type=b'heatmap', datasource_type=b'table', datasource_id=tbl.id, params=textwrap.dedent(b'        {\n            "all_columns_x": "source",\n            "all_columns_y": "target",\n            "canvas_image_rendering": "pixelated",\n            "collapsed_fieldsets": "",\n            "datasource_id": "1",\n            "datasource_name": "energy_usage",\n            "datasource_type": "table",\n            "flt_col_0": "source",\n            "flt_eq_0": "",\n            "flt_op_0": "in",\n            "having": "",\n            "linear_color_scheme": "blue_white_yellow",\n            "metric": "sum__value",\n            "normalize_across": "heatmap",\n            "slice_name": "Heatmap",\n            "viz_type": "heatmap",\n            "where": "",\n            "xscale_interval": "1",\n            "yscale_interval": "1"\n        }\n        '))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)


def load_world_bank_health_n_pop():
    """Loads the world bank health dataset, slices and a dashboard"""
    tbl_name = b'wb_health_population'
    with gzip.open(os.path.join(DATA_FOLDER, b'countries.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.columns = [ col.replace(b'.', b'_') for col in pdf.columns ]
    pdf.year = pd.to_datetime(pdf.year)
    pdf.to_sql(tbl_name, db.engine, if_exists=b'replace', chunksize=50, dtype={b'year': DateTime(), 
       b'country_code': String(3), 
       b'country_name': String(255), 
       b'region': String(255)}, index=False)
    print(b'Creating table [wb_health_population] reference')
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = utils.readfile(os.path.join(DATA_FOLDER, b'countries.md'))
    tbl.main_dttm_col = b'year'
    tbl.is_featured = True
    tbl.database = utils.get_or_create_main_db(caravel)
    db.session.merge(tbl)
    db.session.commit()
    tbl.fetch_metadata()
    defaults = {b'compare_lag': b'10', 
       b'compare_suffix': b'o10Y', 
       b'datasource_id': b'1', 
       b'datasource_name': b'birth_names', 
       b'datasource_type': b'table', 
       b'limit': b'25', 
       b'granularity': b'year', 
       b'groupby': [], b'metric': b'sum__SP_POP_TOTL', 
       b'metrics': [
                  b'sum__SP_POP_TOTL'], 
       b'row_limit': config.get(b'ROW_LIMIT'), 
       b'since': b'2014-01-01', 
       b'until': b'2014-01-01', 
       b'where': b'', 
       b'markup_type': b'markdown', 
       b'country_fieldtype': b'cca3', 
       b'secondary_metric': b'sum__SP_POP_TOTL', 
       b'entity': b'country_code', 
       b'show_bubbles': b'y'}
    print(b'Creating slices')
    slices = [
     Slice(slice_name=b'Region Filter', viz_type=b'filter_box', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'filter_box', groupby=[
      b'region', b'country_name'])),
     Slice(slice_name=b"World's Population", viz_type=b'big_number', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, since=b'2000', viz_type=b'big_number', compare_lag=b'10', metric=b'sum__SP_POP_TOTL', compare_suffix=b'over 10Y')),
     Slice(slice_name=b'Most Populated Countries', viz_type=b'table', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'table', metrics=[
      b'sum__SP_POP_TOTL'], groupby=[
      b'country_name'])),
     Slice(slice_name=b'Growth Rate', viz_type=b'line', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'line', since=b'1960-01-01', metrics=[
      b'sum__SP_POP_TOTL'], num_period_compare=b'10', groupby=[
      b'country_name'])),
     Slice(slice_name=b'% Rural', viz_type=b'world_map', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'world_map', metric=b'sum__SP_RUR_TOTL_ZS', num_period_compare=b'10')),
     Slice(slice_name=b'Life Expectancy VS Rural %', viz_type=b'bubble', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'bubble', since=b'2011-01-01', until=b'2011-01-01', series=b'region', limit=b'0', entity=b'country_name', x=b'sum__SP_RUR_TOTL_ZS', y=b'sum__SP_DYN_LE00_IN', size=b'sum__SP_POP_TOTL', max_bubble_size=b'50', flt_col_1=b'country_code', flt_op_1=b'not in', flt_eq_1=b'TCA,MNP,DMA,MHL,MCO,SXM,CYM,TUV,IMY,KNA,ASM,ADO,AMA,PLW', num_period_compare=b'10')),
     Slice(slice_name=b'Rural Breakdown', viz_type=b'sunburst', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'sunburst', groupby=[
      b'region', b'country_name'], secondary_metric=b'sum__SP_RUR_TOTL', since=b'2011-01-01', until=b'2011-01-01')),
     Slice(slice_name=b"World's Pop Growth", viz_type=b'area', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, since=b'1960-01-01', until=b'now', viz_type=b'area', groupby=[
      b'region'])),
     Slice(slice_name=b'Box plot', viz_type=b'box_plot', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, since=b'1960-01-01', until=b'now', whisker_options=b'Min/max (no outliers)', viz_type=b'box_plot', groupby=[
      b'region'])),
     Slice(slice_name=b'Treemap', viz_type=b'treemap', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, since=b'1960-01-01', until=b'now', viz_type=b'treemap', metrics=[
      b'sum__SP_POP_TOTL'], groupby=[
      b'region', b'country_code'])),
     Slice(slice_name=b'Parallel Coordinates', viz_type=b'para', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, since=b'2011-01-01', until=b'2011-01-01', viz_type=b'para', limit=100, metrics=[
      b'sum__SP_POP_TOTL',
      b'sum__SP_RUR_TOTL_ZS',
      b'sum__SH_DYN_AIDS'], secondary_metric=b'sum__SP_POP_TOTL', series=b'country_name'))]
    misc_dash_slices.append(slices[(-1)].slice_name)
    for slc in slices:
        merge_slice(slc)

    print(b"Creating a World's Health Bank dashboard")
    dash_name = b"World's Bank Data"
    slug = b'world_health'
    dash = db.session.query(Dash).filter_by(slug=slug).first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent(b'    [\n        {\n            "col": 1,\n            "row": 0,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1231"\n        },\n        {\n            "col": 1,\n            "row": 2,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1232"\n        },\n        {\n            "col": 10,\n            "row": 0,\n            "size_x": 3,\n            "size_y": 7,\n            "slice_id": "1233"\n        },\n        {\n            "col": 1,\n            "row": 4,\n            "size_x": 6,\n            "size_y": 3,\n            "slice_id": "1234"\n        },\n        {\n            "col": 3,\n            "row": 0,\n            "size_x": 7,\n            "size_y": 4,\n            "slice_id": "1235"\n        },\n        {\n            "col": 5,\n            "row": 7,\n            "size_x": 8,\n            "size_y": 4,\n            "slice_id": "1236"\n        },\n        {\n            "col": 7,\n            "row": 4,\n            "size_x": 3,\n            "size_y": 3,\n            "slice_id": "1237"\n        },\n        {\n            "col": 1,\n            "row": 7,\n            "size_x": 4,\n            "size_y": 4,\n            "slice_id": "1238"\n        },\n        {\n            "col": 9,\n            "row": 11,\n            "size_x": 4,\n            "size_y": 4,\n            "slice_id": "1239"\n        },\n        {\n            "col": 1,\n            "row": 11,\n            "size_x": 8,\n            "size_y": 4,\n            "slice_id": "1240"\n        }\n    ]\n    ')
    l = json.loads(js)
    for i, pos in enumerate(l):
        pos[b'slice_id'] = str(slices[i].id)

    dash.dashboard_title = dash_name
    dash.position_json = json.dumps(l, indent=4)
    dash.slug = slug
    dash.slices = slices[:-1]
    db.session.merge(dash)
    db.session.commit()


def load_css_templates():
    """Loads 2 css templates to demonstrate the feature"""
    print(b'Creating default CSS templates')
    CSS = models.CssTemplate
    obj = db.session.query(CSS).filter_by(template_name=b'Flat').first()
    if not obj:
        obj = CSS(template_name=b'Flat')
    css = textwrap.dedent(b"    .gridster div.widget {\n        transition: background-color 0.5s ease;\n        background-color: #FAFAFA;\n        border: 1px solid #CCC;\n        box-shadow: none;\n        border-radius: 0px;\n    }\n    .gridster div.widget:hover {\n        border: 1px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .chart-header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
    obj = db.session.query(CSS).filter_by(template_name=b'Courier Black').first()
    if not obj:
        obj = CSS(template_name=b'Courier Black')
    css = textwrap.dedent(b"    .gridster div.widget {\n        transition: background-color 0.5s ease;\n        background-color: #EEE;\n        border: 2px solid #444;\n        border-radius: 15px;\n        box-shadow: none;\n    }\n    h2 {\n        color: white;\n        font-size: 52px;\n    }\n    .navbar {\n        box-shadow: none;\n    }\n    .gridster div.widget:hover {\n        border: 2px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .chart-header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    .nvd3 text {\n        font-size: 12px;\n        font-family: inherit;\n    }\n    body{\n        background: #000;\n        font-family: Courier, Monaco, monospace;;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()


def load_birth_names():
    """Loading birth name dataset from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, b'birth_names.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit=b'ms')
    pdf.to_sql(b'birth_names', db.engine, if_exists=b'replace', chunksize=500, dtype={b'ds': DateTime, 
       b'gender': String(16), 
       b'state': String(10), 
       b'name': String(255)}, index=False)
    l = []
    print(b'Done loading table!')
    print(b'-' * 80)
    print(b'Creating table [birth_names] reference')
    obj = db.session.query(TBL).filter_by(table_name=b'birth_names').first()
    if not obj:
        obj = TBL(table_name=b'birth_names')
    obj.main_dttm_col = b'ds'
    obj.database = utils.get_or_create_main_db(caravel)
    obj.is_featured = True
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    defaults = {b'compare_lag': b'10', 
       b'compare_suffix': b'o10Y', 
       b'datasource_id': b'1', 
       b'datasource_name': b'birth_names', 
       b'datasource_type': b'table', 
       b'flt_op_1': b'in', 
       b'limit': b'25', 
       b'granularity': b'ds', 
       b'groupby': [], b'metric': b'sum__num', 
       b'metrics': [
                  b'sum__num'], 
       b'row_limit': config.get(b'ROW_LIMIT'), 
       b'since': b'100 years ago', 
       b'until': b'now', 
       b'viz_type': b'table', 
       b'where': b'', 
       b'markup_type': b'markdown'}
    print(b'Creating some slices')
    slices = [
     Slice(slice_name=b'Girls', viz_type=b'table', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, groupby=[
      b'name'], flt_col_1=b'gender', flt_eq_1=b'girl', row_limit=50)),
     Slice(slice_name=b'Boys', viz_type=b'table', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, groupby=[
      b'name'], flt_col_1=b'gender', flt_eq_1=b'boy', row_limit=50)),
     Slice(slice_name=b'Participants', viz_type=b'big_number', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'big_number', granularity=b'ds', compare_lag=b'5', compare_suffix=b'over 5Y')),
     Slice(slice_name=b'Genders', viz_type=b'pie', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'pie', groupby=[b'gender'])),
     Slice(slice_name=b'Genders by State', viz_type=b'dist_bar', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, flt_eq_1=b'other', viz_type=b'dist_bar', metrics=[
      b'sum__sum_girls', b'sum__sum_boys'], groupby=[
      b'state'], flt_op_1=b'not in', flt_col_1=b'state')),
     Slice(slice_name=b'Trends', viz_type=b'line', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'line', groupby=[b'name'], granularity=b'ds', rich_tooltip=b'y', show_legend=b'y')),
     Slice(slice_name=b'Title', viz_type=b'markup', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'markup', markup_type=b'html', code=b'<div style="text-align:center">\n    <h1>Birth Names Dashboard</h1>\n    <p>\n        The source dataset came from\n        <a href="https://github.com/hadley/babynames">[here]</a>\n    </p>\n    <img src="/static/assets/images/babytux.jpg">\n</div>\n')),
     Slice(slice_name=b'Name Cloud', viz_type=b'word_cloud', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'word_cloud', size_from=b'10', series=b'name', size_to=b'70', rotation=b'square', limit=b'100')),
     Slice(slice_name=b'Pivot Table', viz_type=b'pivot_table', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'pivot_table', metrics=[b'sum__num'], groupby=[
      b'name'], columns=[b'state'])),
     Slice(slice_name=b'Number of Girls', viz_type=b'big_number_total', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(defaults, viz_type=b'big_number_total', granularity=b'ds', flt_col_1=b'gender', flt_eq_1=b'girl', subheader=b'total female participants'))]
    for slc in slices:
        merge_slice(slc)

    print(b'Creating a dashboard')
    dash = db.session.query(Dash).filter_by(dashboard_title=b'Births').first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent(b'    [\n        {\n            "col": 9,\n            "row": 6,\n            "size_x": 2,\n            "size_y": 4,\n            "slice_id": "1267"\n        },\n        {\n            "col": 11,\n            "row": 6,\n            "size_x": 2,\n            "size_y": 4,\n            "slice_id": "1268"\n        },\n        {\n            "col": 1,\n            "row": 0,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1269"\n        },\n        {\n            "col": 3,\n            "row": 0,\n            "size_x": 2,\n            "size_y": 2,\n            "slice_id": "1270"\n        },\n        {\n            "col": 5,\n            "row": 3,\n            "size_x": 8,\n            "size_y": 3,\n            "slice_id": "1271"\n        },\n        {\n            "col": 1,\n            "row": 6,\n            "size_x": 8,\n            "size_y": 4,\n            "slice_id": "1272"\n        },\n        {\n            "col": 10,\n            "row": 0,\n            "size_x": 3,\n            "size_y": 3,\n            "slice_id": "1273"\n        },\n        {\n            "col": 5,\n            "row": 0,\n            "size_x": 5,\n            "size_y": 3,\n            "slice_id": "1274"\n        },\n        {\n            "col": 1,\n            "row": 2,\n            "size_x": 4,\n            "size_y": 4,\n            "slice_id": "1275"\n        }\n    ]\n        ')
    l = json.loads(js)
    for i, pos in enumerate(l):
        pos[b'slice_id'] = str(slices[i].id)

    dash.dashboard_title = b'Births'
    dash.position_json = json.dumps(l, indent=4)
    dash.slug = b'births'
    dash.slices = slices[:-1]
    db.session.merge(dash)
    db.session.commit()


def load_unicode_test_data():
    """Loading unicode test dataset from a csv file in the repo"""
    df = pd.read_csv(os.path.join(DATA_FOLDER, b'unicode_utf8_unixnl_test.csv'), encoding=b'utf-8')
    df[b'date'] = datetime.datetime.now().date()
    df[b'value'] = [ random.randint(1, 100) for _ in range(len(df)) ]
    df.to_sql(b'unicode_test', db.engine, if_exists=b'replace', chunksize=500, dtype={b'phrase': String(500), 
       b'short_phrase': String(10), 
       b'with_missing': String(100), 
       b'date': Date(), 
       b'value': Float()}, index=False)
    print(b'Done loading table!')
    print(b'-' * 80)
    print(b'Creating table [unicode_test] reference')
    obj = db.session.query(TBL).filter_by(table_name=b'unicode_test').first()
    if not obj:
        obj = TBL(table_name=b'unicode_test')
    obj.main_dttm_col = b'date'
    obj.database = utils.get_or_create_main_db(caravel)
    obj.is_featured = False
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {b'datasource_id': b'3', 
       b'datasource_name': b'unicode_test', 
       b'datasource_type': b'table', 
       b'flt_op_1': b'in', 
       b'granularity': b'date', 
       b'groupby': [], b'metric': b'sum__value', 
       b'row_limit': config.get(b'ROW_LIMIT'), 
       b'since': b'100 years ago', 
       b'until': b'now', 
       b'where': b'', 
       b'viz_type': b'word_cloud', 
       b'size_from': b'10', 
       b'series': b'short_phrase', 
       b'size_to': b'70', 
       b'rotation': b'square', 
       b'limit': b'100'}
    print(b'Creating a slice')
    slc = Slice(slice_name=b'Unicode Cloud', viz_type=b'word_cloud', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(slice_data))
    merge_slice(slc)
    print(b'Creating a dashboard')
    dash = db.session.query(Dash).filter_by(dashboard_title=b'Unicode Test').first()
    if not dash:
        dash = Dash()
    pos = {b'size_y': 4, b'size_x': 4, 
       b'col': 1, 
       b'row': 1, 
       b'slice_id': slc.id}
    dash.dashboard_title = b'Unicode Test'
    dash.position_json = json.dumps([pos], indent=4)
    dash.slug = b'unicode-test'
    dash.slices = [slc]
    db.session.merge(dash)
    db.session.commit()


def load_random_time_series_data():
    """Loading random time series data from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, b'random_time_series.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit=b's')
    pdf.to_sql(b'random_time_series', db.engine, if_exists=b'replace', chunksize=500, dtype={b'ds': DateTime}, index=False)
    print(b'Done loading table!')
    print(b'-' * 80)
    print(b'Creating table [random_time_series] reference')
    obj = db.session.query(TBL).filter_by(table_name=b'random_time_series').first()
    if not obj:
        obj = TBL(table_name=b'random_time_series')
    obj.main_dttm_col = b'ds'
    obj.database = utils.get_or_create_main_db(caravel)
    obj.is_featured = False
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {b'datasource_id': b'6', 
       b'datasource_name': b'random_time_series', 
       b'datasource_type': b'table', 
       b'granularity': b'day', 
       b'row_limit': config.get(b'ROW_LIMIT'), 
       b'since': b'1 year ago', 
       b'until': b'now', 
       b'where': b'', 
       b'viz_type': b'cal_heatmap', 
       b'domain_granularity': b'month', 
       b'subdomain_granularity': b'day'}
    print(b'Creating a slice')
    slc = Slice(slice_name=b'Calendar Heatmap', viz_type=b'cal_heatmap', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(slice_data))
    merge_slice(slc)


def load_long_lat_data():
    """Loading lat/long data from a csv file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, b'san_francisco.csv.gz')) as (f):
        pdf = pd.read_csv(f, encoding=b'utf-8')
    pdf[b'date'] = datetime.datetime.now().date()
    pdf[b'occupancy'] = [ random.randint(1, 6) for _ in range(len(pdf)) ]
    pdf[b'radius_miles'] = [ random.uniform(1, 3) for _ in range(len(pdf)) ]
    pdf.to_sql(b'long_lat', db.engine, if_exists=b'replace', chunksize=500, dtype={b'longitude': Float(), 
       b'latitude': Float(), 
       b'number': Float(), 
       b'street': String(100), 
       b'unit': String(10), 
       b'city': String(50), 
       b'district': String(50), 
       b'region': String(50), 
       b'postcode': Float(), 
       b'id': String(100), 
       b'date': Date(), 
       b'occupancy': Float(), 
       b'radius_miles': Float()}, index=False)
    print(b'Done loading table!')
    print(b'-' * 80)
    print(b'Creating table reference')
    obj = db.session.query(TBL).filter_by(table_name=b'long_lat').first()
    if not obj:
        obj = TBL(table_name=b'long_lat')
    obj.main_dttm_col = b'date'
    obj.database = utils.get_or_create_main_db(caravel)
    obj.is_featured = False
    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    slice_data = {b'datasource_id': b'7', 
       b'datasource_name': b'long_lat', 
       b'datasource_type': b'table', 
       b'granularity': b'day', 
       b'since': b'2014-01-01', 
       b'until': b'2016-12-12', 
       b'where': b'', 
       b'viz_type': b'mapbox', 
       b'all_columns_x': b'LON', 
       b'all_columns_y': b'LAT', 
       b'mapbox_style': b'mapbox://styles/mapbox/light-v9', 
       b'all_columns': [
                      b'occupancy'], 
       b'row_limit': 500000}
    print(b'Creating a slice')
    slc = Slice(slice_name=b'Mapbox Long/Lat', viz_type=b'mapbox', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(slice_data))
    misc_dash_slices.append(slc.slice_name)
    merge_slice(slc)


def load_multiformat_time_series_data():
    """Loading time series data from a zip file in the repo"""
    with gzip.open(os.path.join(DATA_FOLDER, b'multiformat_time_series.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit=b's')
    pdf.ds2 = pd.to_datetime(pdf.ds2, unit=b's')
    pdf.to_sql(b'multiformat_time_series', db.engine, if_exists=b'replace', chunksize=500, dtype={b'ds': Date, 
       b'ds2': DateTime, 
       b'epoch_s': BigInteger, 
       b'epoch_ms': BigInteger, 
       b'string0': String(100), 
       b'string1': String(100), 
       b'string2': String(100), 
       b'string3': String(100)}, index=False)
    print(b'Done loading table!')
    print(b'-' * 80)
    print(b'Creating table [multiformat_time_series] reference')
    obj = db.session.query(TBL).filter_by(table_name=b'multiformat_time_series').first()
    if not obj:
        obj = TBL(table_name=b'multiformat_time_series')
    obj.main_dttm_col = b'ds'
    obj.database = utils.get_or_create_main_db(caravel)
    obj.is_featured = False
    dttm_and_expr_dict = {b'ds': [
             None, None], 
       b'ds2': [
              None, None], 
       b'epoch_s': [
                  b'epoch_s', None], 
       b'epoch_ms': [
                   b'epoch_ms', None], 
       b'string2': [
                  b'%Y%m%d-%H%M%S', None], 
       b'string1': [
                  b'%Y-%m-%d^%H:%M:%S', None], 
       b'string0': [
                  b'%Y-%m-%d %H:%M:%S.%f', None], 
       b'string3': [
                  b'%Y/%m/%d%H:%M:%S.%f', None]}
    for col in obj.table_columns:
        dttm_and_expr = dttm_and_expr_dict[col.column_name]
        col.python_date_format = dttm_and_expr[0]
        col.dbatabase_expr = dttm_and_expr[1]
        col.is_dttm = True

    db.session.merge(obj)
    db.session.commit()
    obj.fetch_metadata()
    tbl = obj
    print(b'Creating some slices')
    for i, col in enumerate(tbl.table_columns):
        slice_data = {b'granularity_sqla': col.column_name, b'datasource_id': b'8', 
           b'datasource_name': b'multiformat_time_series', 
           b'datasource_type': b'table', 
           b'granularity': b'day', 
           b'row_limit': config.get(b'ROW_LIMIT'), 
           b'since': b'1 year ago', 
           b'until': b'now', 
           b'where': b'', 
           b'viz_type': b'cal_heatmap', 
           b'domain_granularity': b'month', 
           b'subdomain_granularity': b'day'}
        slc = Slice(slice_name=b'Calendar Heatmap multiformat ' + str(i), viz_type=b'cal_heatmap', datasource_type=b'table', datasource_id=tbl.id, params=get_slice_json(slice_data))
        merge_slice(slc)

    misc_dash_slices.append(slc.slice_name)
    return


def load_misc_dashboard():
    """Loading a dasbhoard featuring misc charts"""
    print(b'Creating the dashboard')
    db.session.expunge_all()
    DASH_SLUG = b'misc_charts'
    dash = db.session.query(Dash).filter_by(slug=DASH_SLUG).first()
    if not dash:
        dash = Dash()
    js = textwrap.dedent(b'    [\n        {\n            "col": 1,\n            "row": 7,\n            "size_x": 6,\n            "size_y": 4,\n            "slice_id": "442"\n        },\n        {\n            "col": 1,\n            "row": 2,\n            "size_x": 6,\n            "size_y": 5,\n            "slice_id": "443"\n        },\n        {\n            "col": 7,\n            "row": 2,\n            "size_x": 6,\n            "size_y": 4,\n            "slice_id": "444"\n        },\n        {\n            "col": 9,\n            "row": 0,\n            "size_x": 4,\n            "size_y": 2,\n            "slice_id": "455"\n        },\n        {\n            "col": 7,\n            "row": 6,\n            "size_x": 6,\n            "size_y": 5,\n            "slice_id": "467"\n        },\n        {\n            "col": 1,\n            "row": 0,\n            "size_x": 8,\n            "size_y": 2,\n            "slice_id": "475"\n        }\n    ]\n    ')
    l = json.loads(js)
    slices = db.session.query(Slice).filter(Slice.slice_name.in_(misc_dash_slices)).all()
    slices = sorted(slices, key=lambda x: x.id)
    for i, pos in enumerate(l):
        pos[b'slice_id'] = str(slices[i].id)

    dash.dashboard_title = b'Misc Charts'
    dash.position_json = json.dumps(l, indent=4)
    dash.slug = DASH_SLUG
    dash.slices = slices
    db.session.merge(dash)
    db.session.commit()