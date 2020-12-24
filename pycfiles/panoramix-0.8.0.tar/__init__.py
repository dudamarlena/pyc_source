# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxime_beauchemin/code/panoramix/panoramix/data/__init__.py
# Compiled at: 2016-03-05 21:50:23
import gzip, json, os, textwrap, pandas as pd
from sqlalchemy import String, DateTime
from panoramix import app, db, models, utils
DB = models.Database
Slice = models.Slice
TBL = models.SqlaTable
Dash = models.Dashboard
config = app.config
DATA_FOLDER = os.path.join(config.get('BASE_DIR'), 'data')

def get_or_create_db(session):
    print 'Creating database reference'
    dbobj = session.query(DB).filter_by(database_name='main').first()
    if not dbobj:
        dbobj = DB(database_name='main')
    print config.get('SQLALCHEMY_DATABASE_URI')
    dbobj.sqlalchemy_uri = config.get('SQLALCHEMY_DATABASE_URI')
    session.add(dbobj)
    session.commit()
    return dbobj


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


def load_world_bank_health_n_pop():
    tbl_name = 'wb_health_population'
    with gzip.open(os.path.join(DATA_FOLDER, 'countries.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.columns = [ col.replace('.', '_') for col in pdf.columns ]
    pdf.year = pd.to_datetime(pdf.year)
    pdf.to_sql(tbl_name, db.engine, if_exists='replace', chunksize=500, dtype={'year': DateTime(), 
       'country_code': String(3), 
       'country_name': String(255), 
       'region': String(255)}, index=False)
    print 'Creating table [wb_health_population] reference'
    tbl = db.session.query(TBL).filter_by(table_name=tbl_name).first()
    if not tbl:
        tbl = TBL(table_name=tbl_name)
    tbl.description = utils.readfile(os.path.join(DATA_FOLDER, 'countries.md'))
    tbl.main_dttm_col = 'year'
    tbl.is_featured = True
    tbl.database = get_or_create_db(db.session)
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
       'groupby': [], 'metric': 'sum__SP_POP_TOTL', 
       'metrics': [
                 'sum__SP_POP_TOTL'], 
       'row_limit': config.get('ROW_LIMIT'), 
       'since': '2014-01-01', 
       'until': '2014-01-01', 
       'where': '', 
       'markup_type': 'markdown', 
       'country_fieldtype': 'cca3', 
       'secondary_metric': 'sum__SP_POP_TOTL', 
       'entity': 'country_code', 
       'show_bubbles': 'y'}
    print 'Creating slices'
    slices = [
     Slice(slice_name='Region Filter', viz_type='filter_box', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='filter_box', groupby=[
      'region'])),
     Slice(slice_name="World's Population", viz_type='big_number', datasource_type='table', table=tbl, params=get_slice_json(defaults, since='2000', viz_type='big_number', compare_lag='10', metric='sum__SP_POP_TOTL', compare_suffix='over 10Y')),
     Slice(slice_name='Most Populated Countries', viz_type='table', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='table', metrics=[
      'sum__SP_POP_TOTL'], groupby=[
      'country_name'])),
     Slice(slice_name='Growth Rate', viz_type='line', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='line', since='1960-01-01', metrics=[
      'sum__SP_POP_TOTL'], num_period_compare='10', groupby=[
      'country_name'])),
     Slice(slice_name='% Rural', viz_type='world_map', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='world_map', metric='sum__SP_RUR_TOTL_ZS', num_period_compare='10')),
     Slice(slice_name='Life Expexctancy VS Rural %', viz_type='bubble', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='bubble', since='2011-01-01', until='2011-01-01', series='region', limit='0', entity='country_name', x='sum__SP_RUR_TOTL_ZS', y='sum__SP_DYN_LE00_IN', size='sum__SP_POP_TOTL', max_bubble_size='50', flt_col_1='country_code', flt_op_1='not in', flt_eq_1='TCA,MNP,DMA,MHL,MCO,SXM,CYM,TUV,IMY,KNA,ASM,ADO,AMA,PLW', num_period_compare='10')),
     Slice(slice_name='Rural Breakdown', viz_type='sunburst', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='sunburst', groupby=[
      'region', 'country_name'], secondary_metric='sum__SP_RUR_TOTL', since='2011-01-01', until='2011-01-01')),
     Slice(slice_name="World's Pop Growth", viz_type='area', datasource_type='table', table=tbl, params=get_slice_json(defaults, since='1960-01-01', until='now', viz_type='area', groupby=[
      'region']))]
    for slc in slices:
        merge_slice(slc)

    print "Creating a World's Health Bank dashboard"
    dash_name = "World's Health Bank Dashboard"
    dash = db.session.query(Dash).filter_by(dashboard_title=dash_name).first()
    if dash:
        db.session.delete(dash)
    js = '[\n    {\n        "size_y": 1,\n        "size_x": 3,\n        "col": 1,\n        "slice_id": "269",\n        "row": 1\n    },\n    {\n        "size_y": 3,\n        "size_x": 3,\n        "col": 1,\n        "slice_id": "270",\n        "row": 2\n    },\n    {\n        "size_y": 7,\n        "size_x": 3,\n        "col": 10,\n        "slice_id": "271",\n        "row": 1\n    },\n    {\n        "size_y": 3,\n        "size_x": 6,\n        "col": 1,\n        "slice_id": "272",\n        "row": 5\n    },\n    {\n        "size_y": 4,\n        "size_x": 6,\n        "col": 4,\n        "slice_id": "273",\n        "row": 1\n    },\n    {\n        "size_y": 4,\n        "size_x": 6,\n        "col": 7,\n        "slice_id": "274",\n        "row": 8\n    },\n    {\n        "size_y": 3,\n        "size_x": 3,\n        "col": 7,\n        "slice_id": "275",\n        "row": 5\n    },\n    {\n        "size_y": 4,\n        "size_x": 6,\n        "col": 1,\n        "slice_id": "276",\n        "row": 8\n    }\n]\n    '
    l = json.loads(js)
    for i, pos in enumerate(l):
        pos['slice_id'] = str(slices[i].id)

    dash = Dash(dashboard_title=dash_name, position_json=json.dumps(l, indent=4))
    for s in slices:
        dash.slices.append(s)

    db.session.commit()


def load_birth_names():
    session = db.session
    with gzip.open(os.path.join(DATA_FOLDER, 'birth_names.json.gz')) as (f):
        pdf = pd.read_json(f)
    pdf.ds = pd.to_datetime(pdf.ds, unit='ms')
    pdf.to_sql('birth_names', db.engine, if_exists='replace', chunksize=500, dtype={'ds': DateTime, 
       'gender': String(16), 
       'state': String(10), 
       'name': String(255)}, index=False)
    l = []
    print 'Done loading table!'
    print '-' * 80
    print 'Creating default CSS templates'
    CSS = models.CssTemplate
    obj = db.session.query(CSS).filter_by(template_name='Flat').first()
    if not obj:
        obj = CSS(template_name='Flat')
    css = textwrap.dedent("    .gridster li.widget {\n        transition: background-color 0.5s ease;\n        background-color: #FAFAFA;\n        border: 1px solid #CCC;\n        overflow: hidden;\n        box-shadow: none;\n        border-radius: 0px;\n    }\n    .gridster li.widget:hover {\n        border: 1px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .slice_header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
    obj = db.session.query(CSS).filter_by(template_name='Courier Black').first()
    if not obj:
        obj = CSS(template_name='Courier Black')
    css = textwrap.dedent("    .gridster li.widget {\n        transition: background-color 0.5s ease;\n        background-color: #EEE;\n        border: 2px solid #444;\n        overflow: hidden;\n        border-radius: 15px;\n        box-shadow: none;\n    }\n    h2 {\n        color: white;\n        font-size: 52px;\n    }\n    .navbar {\n        box-shadow: none;\n    }\n    .gridster li.widget:hover {\n        border: 2px solid #000;\n        background-color: #EAEAEA;\n    }\n    .navbar {\n        transition: opacity 0.5s ease;\n        opacity: 0.05;\n    }\n    .navbar:hover {\n        opacity: 1;\n    }\n    .slice_header .header{\n        font-weight: normal;\n        font-size: 12px;\n    }\n    .nvd3 text {\n        font-size: 12px;\n        font-family: inherit;\n    }\n    body{\n        background: #000;\n        font-family: Courier, Monaco, monospace;;\n    }\n    /*\n    var bnbColors = [\n        //rausch    hackb      kazan      babu      lima        beach     tirol\n        '#ff5a5f', '#7b0051', '#007A87', '#00d1c1', '#8ce071', '#ffb400', '#b4a76c',\n        '#ff8083', '#cc0086', '#00a1b3', '#00ffeb', '#bbedab', '#ffd266', '#cbc29a',\n        '#ff3339', '#ff1ab1', '#005c66', '#00b3a5', '#55d12e', '#b37e00', '#988b4e',\n     ];\n    */\n    ")
    obj.css = css
    db.session.merge(obj)
    db.session.commit()
    print 'Creating table reference'
    obj = db.session.query(TBL).filter_by(table_name='birth_names').first()
    if not obj:
        obj = TBL(table_name='birth_names')
    obj.main_dttm_col = 'ds'
    obj.database = get_or_create_db(db.session)
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
       'groupby': [], 'metric': 'sum__num', 
       'metrics': [
                 'sum__num'], 
       'row_limit': config.get('ROW_LIMIT'), 
       'since': '100 years ago', 
       'until': 'now', 
       'viz_type': 'table', 
       'where': '', 
       'markup_type': 'markdown'}
    print 'Creating some slices'
    slices = [
     Slice(slice_name='Girls', viz_type='table', datasource_type='table', table=tbl, params=get_slice_json(defaults, groupby=[
      'name'], flt_col_1='gender', flt_eq_1='girl', row_limit=50)),
     Slice(slice_name='Boys', viz_type='table', datasource_type='table', table=tbl, params=get_slice_json(defaults, groupby=[
      'name'], flt_col_1='gender', flt_eq_1='boy', row_limit=50)),
     Slice(slice_name='Participants', viz_type='big_number', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='big_number', granularity='ds', compare_lag='5', compare_suffix='over 5Y')),
     Slice(slice_name='Genders', viz_type='pie', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='pie', groupby=['gender'])),
     Slice(slice_name='Genders by State', viz_type='dist_bar', datasource_type='table', table=tbl, params=get_slice_json(defaults, flt_eq_1='other', viz_type='dist_bar', metrics=[
      'sum__sum_girls', 'sum__sum_boys'], groupby=[
      'state'], flt_op_1='not in', flt_col_1='state')),
     Slice(slice_name='Trends', viz_type='line', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='line', groupby=['name'], granularity='ds', rich_tooltip='y', show_legend='y')),
     Slice(slice_name='Title', viz_type='markup', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='markup', markup_type='html', code='    <div style="text-align:center">\n        <h1>Birth Names Dashboard</h1>\n        <p>The source dataset came from <a href="https://github.com/hadley/babynames">[here]</a></p>\n        <img src="http://monblog.system-linux.net/image/tux/baby-tux_overlord59-tux.png">\n    </div>\n    ')),
     Slice(slice_name='Name Cloud', viz_type='word_cloud', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='word_cloud', size_from='10', series='name', size_to='70', rotation='square', limit='100')),
     Slice(slice_name='Pivot Table', viz_type='pivot_table', datasource_type='table', table=tbl, params=get_slice_json(defaults, viz_type='pivot_table', metrics=['sum__num'], groupby=[
      'name'], columns=['state']))]
    for slc in slices:
        merge_slice(slc)

    print 'Creating a dashboard'
    dash = session.query(Dash).filter_by(dashboard_title='Births').first()
    if dash:
        db.session.delete(dash)
    js = '\n[\n    {\n        "size_y": 4,\n        "size_x": 2,\n        "col": 8,\n        "slice_id": "85",\n        "row": 7\n    },\n    {\n        "size_y": 4,\n        "size_x": 2,\n        "col": 10,\n        "slice_id": "86",\n        "row": 7\n    },\n    {\n        "size_y": 2,\n        "size_x": 2,\n        "col": 1,\n        "slice_id": "87",\n        "row": 1\n    },\n    {\n        "size_y": 2,\n        "size_x": 2,\n        "col": 3,\n        "slice_id": "88",\n        "row": 1\n    },\n    {\n        "size_y": 3,\n        "size_x": 7,\n        "col": 5,\n        "slice_id": "89",\n        "row": 4\n    },\n    {\n        "size_y": 4,\n        "size_x": 7,\n        "col": 1,\n        "slice_id": "90",\n        "row": 7\n    },\n    {\n        "size_y": 3,\n        "size_x": 3,\n        "col": 9,\n        "slice_id": "91",\n        "row": 1\n    },\n    {\n        "size_y": 3,\n        "size_x": 4,\n        "col": 5,\n        "slice_id": "92",\n        "row": 1\n    },\n    {\n        "size_y": 4,\n        "size_x": 4,\n        "col": 1,\n        "slice_id": "93",\n        "row": 3\n    }\n]\n        '
    l = json.loads(js)
    for i, pos in enumerate(l):
        pos['slice_id'] = str(slices[i].id)

    dash = Dash(dashboard_title='Births', position_json=json.dumps(l, indent=4))
    for s in slices:
        dash.slices.append(s)

    session.commit()