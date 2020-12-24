# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/bogdankyryliuk/src/oss/incubator-superset/superset/examples/deck.py
# Compiled at: 2020-01-16 19:49:16
# Size of source mod 2**32: 15361 bytes
import json
from superset import db
from superset.models.dashboard import Dashboard
from superset.models.slice import Slice
from .helpers import get_slice_json, merge_slice, TBL, update_slice_ids
COLOR_RED = {'r':205, 
 'g':0,  'b':3,  'a':0.82}
POSITION_JSON = '{\n    "CHART-3afd9d70": {\n        "meta": {\n            "chartId": 66,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-3afd9d70",\n        "children": []\n    },\n    "CHART-2ee7fa5e": {\n        "meta": {\n            "chartId": 67,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-2ee7fa5e",\n        "children": []\n    },\n    "CHART-201f7715": {\n        "meta": {\n            "chartId": 68,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-201f7715",\n        "children": []\n    },\n    "CHART-d02f6c40": {\n        "meta": {\n            "chartId": 69,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-d02f6c40",\n        "children": []\n    },\n    "CHART-2673431d": {\n        "meta": {\n            "chartId": 70,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-2673431d",\n        "children": []\n    },\n    "CHART-85265a60": {\n        "meta": {\n            "chartId": 71,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-85265a60",\n        "children": []\n    },\n    "CHART-2b87513c": {\n        "meta": {\n            "chartId": 72,\n            "width": 6,\n            "height": 50\n        },\n        "type": "CHART",\n        "id": "CHART-2b87513c",\n        "children": []\n    },\n    "GRID_ID": {\n        "type": "GRID",\n        "id": "GRID_ID",\n        "children": [\n            "ROW-a7b16cb5",\n            "ROW-72c218a5",\n            "ROW-957ba55b",\n            "ROW-af041bdd"\n        ]\n    },\n    "HEADER_ID": {\n        "meta": {\n            "text": "deck.gl Demo"\n        },\n        "type": "HEADER",\n        "id": "HEADER_ID"\n    },\n    "ROOT_ID": {\n        "type": "ROOT",\n        "id": "ROOT_ID",\n        "children": [\n            "GRID_ID"\n        ]\n    },\n    "ROW-72c218a5": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-72c218a5",\n        "children": [\n            "CHART-d02f6c40",\n            "CHART-201f7715"\n        ]\n    },\n    "ROW-957ba55b": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-957ba55b",\n        "children": [\n            "CHART-2673431d",\n            "CHART-85265a60"\n        ]\n    },\n    "ROW-a7b16cb5": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-a7b16cb5",\n        "children": [\n            "CHART-3afd9d70",\n            "CHART-2ee7fa5e"\n        ]\n    },\n    "ROW-af041bdd": {\n        "meta": {\n            "background": "BACKGROUND_TRANSPARENT"\n        },\n        "type": "ROW",\n        "id": "ROW-af041bdd",\n        "children": [\n            "CHART-2b87513c"\n        ]\n    },\n    "DASHBOARD_VERSION_KEY": "v2"\n}'

def load_deck_dash():
    print('Loading deck.gl dashboard')
    slices = []
    tbl = db.session.query(TBL).filter_by(table_name='long_lat').first()
    slice_data = {'spatial':{'type':'latlong', 
      'lonCol':'LON',  'latCol':'LAT'}, 
     'color_picker':COLOR_RED, 
     'datasource':'5__table', 
     'granularity_sqla':None, 
     'groupby':[],  'mapbox_style':'mapbox://styles/mapbox/light-v9', 
     'multiplier':10, 
     'point_radius_fixed':{'type':'metric', 
      'value':'count'}, 
     'point_unit':'square_m', 
     'min_radius':1, 
     'max_radius':250, 
     'row_limit':5000, 
     'time_range':' : ', 
     'size':'count', 
     'time_grain_sqla':None, 
     'viewport':{'bearing':-4.952916738791771, 
      'latitude':37.78926922909199, 
      'longitude':-122.42613341901688, 
      'pitch':4.750411100577438, 
      'zoom':12.729132798697304}, 
     'viz_type':'deck_scatter'}
    print('Creating Scatterplot slice')
    slc = Slice(slice_name='Scatterplot',
      viz_type='deck_scatter',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    slice_data = {'point_unit':'square_m', 
     'row_limit':5000, 
     'spatial':{'type':'latlong', 
      'lonCol':'LON',  'latCol':'LAT'}, 
     'mapbox_style':'mapbox://styles/mapbox/dark-v9', 
     'granularity_sqla':None, 
     'size':'count', 
     'viz_type':'deck_screengrid', 
     'time_range':'No filter', 
     'point_radius':'Auto', 
     'color_picker':{'a':1, 
      'r':14,  'b':0,  'g':255}, 
     'grid_size':20, 
     'viewport':{'zoom':14.161641703941438, 
      'longitude':-122.41827069521386, 
      'bearing':-4.952916738791771, 
      'latitude':37.76024135844065, 
      'pitch':4.750411100577438}, 
     'point_radius_fixed':{'type':'fix', 
      'value':2000}, 
     'datasource':'5__table', 
     'time_grain_sqla':None, 
     'groupby':[]}
    print('Creating Screen Grid slice')
    slc = Slice(slice_name='Screen grid',
      viz_type='deck_screengrid',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    slice_data = {'spatial':{'type':'latlong', 
      'lonCol':'LON',  'latCol':'LAT'}, 
     'row_limit':5000, 
     'mapbox_style':'mapbox://styles/mapbox/streets-v9', 
     'granularity_sqla':None, 
     'size':'count', 
     'viz_type':'deck_hex', 
     'time_range':'No filter', 
     'point_radius_unit':'Pixels', 
     'point_radius':'Auto', 
     'color_picker':{'a':1, 
      'r':14,  'b':0,  'g':255}, 
     'grid_size':40, 
     'extruded':True, 
     'viewport':{'latitude':37.789795085160335, 
      'pitch':54.08961642447763, 
      'zoom':13.835465702403654, 
      'longitude':-122.40632230075536, 
      'bearing':-2.3984797349335167}, 
     'point_radius_fixed':{'type':'fix', 
      'value':2000}, 
     'datasource':'5__table', 
     'time_grain_sqla':None, 
     'groupby':[]}
    print('Creating Hex slice')
    slc = Slice(slice_name='Hexagons',
      viz_type='deck_hex',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    slice_data = {'spatial':{'type':'latlong', 
      'lonCol':'LON',  'latCol':'LAT'}, 
     'row_limit':5000, 
     'mapbox_style':'mapbox://styles/mapbox/satellite-streets-v9', 
     'granularity_sqla':None, 
     'size':'count', 
     'viz_type':'deck_grid', 
     'point_radius_unit':'Pixels', 
     'point_radius':'Auto', 
     'time_range':'No filter', 
     'color_picker':{'a':1, 
      'r':14,  'b':0,  'g':255}, 
     'grid_size':120, 
     'extruded':True, 
     'viewport':{'longitude':-122.42066918995666, 
      'bearing':155.80099696026355, 
      'zoom':12.699690845482069, 
      'latitude':37.7942314882596, 
      'pitch':53.470800300695146}, 
     'point_radius_fixed':{'type':'fix', 
      'value':2000}, 
     'datasource':'5__table', 
     'time_grain_sqla':None, 
     'groupby':[]}
    print('Creating Grid slice')
    slc = Slice(slice_name='Grid',
      viz_type='deck_grid',
      datasource_type='table',
      datasource_id=(tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    polygon_tbl = db.session.query(TBL).filter_by(table_name='sf_population_polygons').first()
    slice_data = {'datasource':'11__table', 
     'viz_type':'deck_polygon', 
     'slice_id':41, 
     'granularity_sqla':None, 
     'time_grain_sqla':None, 
     'time_range':' : ', 
     'line_column':'contour', 
     'metric':{'aggregate':'SUM', 
      'column':{'column_name':'population', 
       'description':None, 
       'expression':None, 
       'filterable':True, 
       'groupby':True, 
       'id':1332, 
       'is_dttm':False, 
       'optionName':'_col_population', 
       'python_date_format':None, 
       'type':'BIGINT', 
       'verbose_name':None}, 
      'expressionType':'SIMPLE', 
      'fromFormData':True, 
      'hasCustomLabel':True, 
      'label':'Population', 
      'optionName':'metric_t2v4qbfiz1_w6qgpx4h2p', 
      'sqlExpression':None}, 
     'line_type':'json', 
     'linear_color_scheme':'oranges', 
     'mapbox_style':'mapbox://styles/mapbox/light-v9', 
     'viewport':{'longitude':-122.43388541747726, 
      'latitude':37.752020331384834, 
      'zoom':11.133995608594631, 
      'bearing':37.89506450385642, 
      'pitch':60, 
      'width':667, 
      'height':906, 
      'altitude':1.5, 
      'maxZoom':20, 
      'minZoom':0, 
      'maxPitch':60, 
      'minPitch':0, 
      'maxLatitude':85.05113, 
      'minLatitude':-85.05113}, 
     'reverse_long_lat':False, 
     'fill_color_picker':{'r':3, 
      'g':65,  'b':73,  'a':1}, 
     'stroke_color_picker':{'r':0, 
      'g':122,  'b':135,  'a':1}, 
     'filled':True, 
     'stroked':False, 
     'extruded':True, 
     'multiplier':0.1, 
     'point_radius_fixed':{'type':'metric', 
      'value':{'aggregate':None, 
       'column':None, 
       'expressionType':'SQL', 
       'fromFormData':None, 
       'hasCustomLabel':None, 
       'label':'Density', 
       'optionName':'metric_c5rvwrzoo86_293h6yrv2ic', 
       'sqlExpression':'SUM(population)/SUM(area)'}}, 
     'js_columns':[],  'js_data_mutator':'', 
     'js_tooltip':'', 
     'js_onclick_href':'', 
     'legend_format':'.1s', 
     'legend_position':'tr'}
    print('Creating Polygon slice')
    slc = Slice(slice_name='Polygons',
      viz_type='deck_polygon',
      datasource_type='table',
      datasource_id=(polygon_tbl.id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    slice_data = {'datasource':'10__table', 
     'viz_type':'deck_arc', 
     'slice_id':42, 
     'granularity_sqla':None, 
     'time_grain_sqla':None, 
     'time_range':' : ', 
     'start_spatial':{'type':'latlong', 
      'latCol':'LATITUDE', 
      'lonCol':'LONGITUDE'}, 
     'end_spatial':{'type':'latlong', 
      'latCol':'LATITUDE_DEST', 
      'lonCol':'LONGITUDE_DEST'}, 
     'row_limit':5000, 
     'mapbox_style':'mapbox://styles/mapbox/light-v9', 
     'viewport':{'altitude':1.5, 
      'bearing':8.546256357301871, 
      'height':642, 
      'latitude':44.596651438714254, 
      'longitude':-91.84340711201104, 
      'maxLatitude':85.05113, 
      'maxPitch':60, 
      'maxZoom':20, 
      'minLatitude':-85.05113, 
      'minPitch':0, 
      'minZoom':0, 
      'pitch':60, 
      'width':997, 
      'zoom':2.929837070560775}, 
     'color_picker':{'r':0, 
      'g':122,  'b':135,  'a':1}, 
     'stroke_width':1}
    print('Creating Arc slice')
    slc = Slice(slice_name='Arcs',
      viz_type='deck_arc',
      datasource_type='table',
      datasource_id=(db.session.query(TBL).filter_by(table_name='flights').first().id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    slice_data = {'datasource':'12__table', 
     'slice_id':43, 
     'viz_type':'deck_path', 
     'time_grain_sqla':None, 
     'time_range':' : ', 
     'line_column':'path_json', 
     'line_type':'json', 
     'row_limit':5000, 
     'mapbox_style':'mapbox://styles/mapbox/light-v9', 
     'viewport':{'longitude':-122.18885402582598, 
      'latitude':37.73671752604488, 
      'zoom':9.51847667620428, 
      'bearing':0, 
      'pitch':0, 
      'width':669, 
      'height':1094, 
      'altitude':1.5, 
      'maxZoom':20, 
      'minZoom':0, 
      'maxPitch':60, 
      'minPitch':0, 
      'maxLatitude':85.05113, 
      'minLatitude':-85.05113}, 
     'color_picker':{'r':0, 
      'g':122,  'b':135,  'a':1}, 
     'line_width':150, 
     'reverse_long_lat':False, 
     'js_columns':[
      'color'], 
     'js_data_mutator':'data => data.map(d => ({\n    ...d,\n    color: colors.hexToRGB(d.extraProps.color)\n}));', 
     'js_tooltip':'', 
     'js_onclick_href':''}
    print('Creating Path slice')
    slc = Slice(slice_name='Path',
      viz_type='deck_path',
      datasource_type='table',
      datasource_id=(db.session.query(TBL).filter_by(table_name='bart_lines').first().id),
      params=(get_slice_json(slice_data)))
    merge_slice(slc)
    slices.append(slc)
    slug = 'deck'
    print('Creating a dashboard')
    title = 'deck.gl Demo'
    dash = db.session.query(Dashboard).filter_by(slug=slug).first()
    if not dash:
        dash = Dashboard()
    dash.published = True
    js = POSITION_JSON
    pos = json.loads(js)
    update_slice_ids(pos, slices)
    dash.position_json = json.dumps(pos, indent=4)
    dash.dashboard_title = title
    dash.slug = slug
    dash.slices = slices
    db.session.merge(dash)
    db.session.commit()


if __name__ == '__main__':
    load_deck_dash()