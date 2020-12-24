# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintxrest/wintxflaskapp.py
# Compiled at: 2016-03-23 14:50:19
from datetime import datetime
from flask import Flask, json, jsonify, request, abort
from flask.ext.cors import CORS
from functools import wraps
import logging
from logging import FileHandler
import sys
from wintx import WintxError
from wintx.interfaces import Query
from wintxrest import default_settings
app = Flask(__name__)
app.config.from_object(default_settings.Config)
app.config.from_envvar('WINTXREST_SETTINGS', silent=True)
cors = CORS(app, resources='*', allow_headers='Content-Type')
QUERY_COLUMNS = [
 'datatype', 'latitude', 'level', 'leveltype', 'longitude', 'time', 'varname']
QUERY_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
wintxConfigFile = app.config['WINTX_CONFIG']
logFile = app.config['LOG_FILE']
logLevel = logging.getLevelName(app.config['LOG_LEVEL'])
useReloader = app.config['RELOADER']
useDebugger = app.config['DEBUGGER']
logfile_handler = FileHandler(logFile)
logfile_handler.setLevel(logLevel)
app.logger.addHandler(logfile_handler)

def formQuery--- This code section failed: ---

 L.  59         0  LOAD_GLOBAL           0  'json'
                3  LOAD_ATTR             1  'loads'
                6  LOAD_FAST             0  'query_string'
                9  LOAD_ATTR             2  'replace'
               12  LOAD_CONST               "'"
               15  LOAD_CONST               '"'
               18  CALL_FUNCTION_2       2  None
               21  CALL_FUNCTION_1       1  None
               24  STORE_FAST            1  'query_dict_given'

 L.  60        27  BUILD_MAP             0 
               30  STORE_FAST            2  'query_dict'

 L.  61        33  LOAD_GLOBAL           3  'type'
               36  LOAD_FAST             1  'query_dict_given'
               39  CALL_FUNCTION_1       1  None
               42  LOAD_GLOBAL           3  'type'
               45  BUILD_MAP             0 
               48  CALL_FUNCTION_1       1  None
               51  COMPARE_OP            3  !=
               54  JUMP_IF_FALSE        14  'to 71'
             57_0  THEN                     72
               57  POP_TOP          

 L.  62        58  LOAD_GLOBAL           4  'abort'
               61  LOAD_CONST               400
               64  CALL_FUNCTION_1       1  None
               67  POP_TOP          
               68  JUMP_FORWARD          1  'to 72'
             71_0  COME_FROM            54  '54'
               71  POP_TOP          
             72_0  COME_FROM            68  '68'

 L.  64        72  SETUP_LOOP          196  'to 271'
               75  LOAD_FAST             1  'query_dict_given'
               78  GET_ITER         
               79  FOR_ITER            188  'to 270'
               82  STORE_FAST            3  'column'

 L.  65        85  LOAD_FAST             3  'column'
               88  LOAD_GLOBAL           5  'QUERY_COLUMNS'
               91  COMPARE_OP            6  in
               94  JUMP_IF_FALSE       159  'to 256'
               97  POP_TOP          

 L.  66        98  LOAD_FAST             3  'column'
              101  LOAD_CONST               'time'
              104  COMPARE_OP            2  ==
              107  JUMP_IF_FALSE       128  'to 238'
              110  POP_TOP          

 L.  67       111  LOAD_GLOBAL           3  'type'
              114  LOAD_FAST             1  'query_dict_given'
              117  LOAD_FAST             3  'column'
              120  BINARY_SUBSCR    
              121  CALL_FUNCTION_1       1  None
              124  LOAD_GLOBAL           3  'type'
              127  BUILD_MAP             0 
              130  CALL_FUNCTION_1       1  None
              133  COMPARE_OP            2  ==
              136  JUMP_IF_FALSE        69  'to 208'
              139  POP_TOP          

 L.  68       140  BUILD_MAP             0 
              143  LOAD_FAST             2  'query_dict'
              146  LOAD_FAST             3  'column'
              149  STORE_SUBSCR     

 L.  69       150  SETUP_LOOP           82  'to 235'
              153  LOAD_FAST             1  'query_dict_given'
              156  LOAD_FAST             3  'column'
              159  BINARY_SUBSCR    
              160  GET_ITER         
              161  FOR_ITER             40  'to 204'
              164  STORE_FAST            4  'comparison'

 L.  70       167  LOAD_GLOBAL           6  'datetime'
              170  LOAD_ATTR             7  'strptime'
              173  LOAD_FAST             1  'query_dict_given'
              176  LOAD_FAST             3  'column'
              179  BINARY_SUBSCR    
              180  LOAD_FAST             4  'comparison'
              183  BINARY_SUBSCR    
              184  LOAD_GLOBAL           8  'QUERY_DATETIME_FORMAT'
              187  CALL_FUNCTION_2       2  None
              190  LOAD_FAST             2  'query_dict'
              193  LOAD_FAST             3  'column'
              196  BINARY_SUBSCR    
              197  LOAD_FAST             4  'comparison'
              200  STORE_SUBSCR     
              201  JUMP_BACK           161  'to 161'
              204  POP_BLOCK        
              205  JUMP_ABSOLUTE       253  'to 253'
            208_0  COME_FROM           136  '136'
              208  POP_TOP          

 L.  72       209  LOAD_GLOBAL           6  'datetime'
              212  LOAD_ATTR             7  'strptime'
              215  LOAD_FAST             1  'query_dict_given'
              218  LOAD_FAST             3  'column'
              221  BINARY_SUBSCR    
              222  LOAD_GLOBAL           8  'QUERY_DATETIME_FORMAT'
              225  CALL_FUNCTION_2       2  None
              228  LOAD_FAST             2  'query_dict'
              231  LOAD_FAST             3  'column'
              234  STORE_SUBSCR     
            235_0  COME_FROM           150  '150'
              235  JUMP_ABSOLUTE       267  'to 267'
            238_0  COME_FROM           107  '107'
              238  POP_TOP          

 L.  74       239  LOAD_FAST             1  'query_dict_given'
              242  LOAD_FAST             3  'column'
              245  BINARY_SUBSCR    
              246  LOAD_FAST             2  'query_dict'
              249  LOAD_FAST             3  'column'
              252  STORE_SUBSCR     
              253  JUMP_BACK            79  'to 79'
            256_0  COME_FROM            94  '94'
              256  POP_TOP          

 L.  77       257  LOAD_GLOBAL           4  'abort'
              260  LOAD_CONST               400
              263  CALL_FUNCTION_1       1  None
              266  POP_TOP          
              267  JUMP_BACK            79  'to 79'
              270  POP_BLOCK        
            271_0  COME_FROM            72  '72'

 L.  79       271  LOAD_FAST             2  'query_dict'
              274  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_ABSOLUTE' instruction at offset 235


def formSort(sort_string):
    sort_list_given = json.loads(sort_string.replace("'", '"'))
    sort_list = []
    if type(sort_list_given) != type([]):
        abort(400)
    for column in sort_list_given:
        if type(column) != type([]):
            abort(400)
        if len(column) != 2:
            abort(400)
        if column[1] != 'asc' and column[1] != 'dsc':
            abort(400)
        if column[0] not in QUERY_COLUMNS:
            abort(400)
        sort_list.append((column[0], column[1]))

    return sort_list


def prepareReturnRecords(records):
    for record in records:
        o_time = record['time']
        record['time'] = o_time.strftime(QUERY_DATETIME_FORMAT)

    return records


def formatReturnTime(r_time):
    return r_time.strftime(QUERY_DATETIME_FORMAT)


def getWintxInstance():
    try:
        wintx_instance = Query(wintxConfigFile)
    except WintxError, err:
        abort(500, 'Can not form backend')

    return wintx_instance


@app.errorhandler(404)
def page_not_found(error):
    return (jsonify({'error': 'Function not found'}), 404)


def authorizeCheck():
    return (
     True, None)


def authorize(func):

    @wraps(func)
    def decorated(*args, **kwargs):
        (authorized, response) = authorizeCheck()
        if not authorized:
            return response
        return func(*args, **kwargs)

    return decorated


@app.route('/query', methods=['GET'])
@authorize
def query():
    """Request - query, sort"""
    query_dict = {}
    if 'query' in request.args:
        query_dict = formQuery(request.args['query'])
    sort_list = None
    if 'sort' in request.args:
        sort_list = formSort(request.args['sort'])
    records = None
    wintx_instance = getWintxInstance()
    try:
        records = wintx_instance.query(query_dict, sort_column=sort_list)
    except WintxError, err:
        return (
         jsonify({'error': err.message}), 500)

    records = prepareReturnRecords(records)
    return (
     jsonify({'records': records}), 200)


@app.route('/query/polygon', methods=['GET'])
@authorize
def query_polygon():
    """Request - query, sort, polygon, invert"""
    if 'polygon' not in request.args:
        abort(400)
    polygon = json.loads(request.args['polygon'].replace("'", '"'))
    if type(polygon) != type([]):
        abort(400)
    for point in polygon:
        if type(point) != type([]) or len(point) != 2:
            abort(400)

    query_dict = {}
    if 'query' in request.args:
        query_dict = formQuery(request.args['query'])
    sort_list = None
    if 'sort' in request.args:
        sort_list = formSort(request.args['sort'])
    invert_points = False
    if 'invert' in request.args:
        invert_points = json.loads(request.args['invert'].replace("'", '"'))
        if type(invert_points) != type(True):
            abort(400)
    records = None
    wintx_instance = getWintxInstance()
    try:
        records = wintx_instance.queryWithin(polygon, query_dict, reverse_points=invert_points, sort_column=sort_list)
    except WintxError, err:
        return (
         jsonify({'error': err.message}), 500)

    records = prepareReturnRecords(records)
    return (
     jsonify({'records': records}), 200)


@app.route('/metadata/times', methods=['GET'])
@authorize
def metadata_times():
    wintx_instance = getWintxInstance()
    return_times = []
    try:
        times = wintx_instance.getTimes()
        for t in times:
            return_times.append(formatReturnTime(t))

    except WintxError, err:
        return (
         jsonify({'error': err.message}), 200)

    return (
     jsonify({'times': return_times}), 200)


@app.route('/metadata/variables/time', methods=['GET'])
@authorize
def metadata_get_variables_at_time():
    variables = None
    corrected_vars = {}
    time = None
    time_end = None
    if 'time' in request.args:
        time = datetime.strptime(request.args['time'], QUERY_DATETIME_FORMAT)
    else:
        abort(400)
    if 'time_end' in request.args:
        time_end = datetime.strptime(request.args['time_end'], QUERY_DATETIME_FORMAT)
    wintx_instance = getWintxInstance()
    try:
        variables = wintx_instance.getVarnamesAtTime(time, time_end=time_end)
        for time in variables:
            t = formatReturnTime(time)
            corrected_vars[t] = variables[time]

    except WintxError, err:
        return jsonify({'error': err.message})

    return (
     jsonify(corrected_vars), 200)


@app.route('/metadata/variables', methods=['GET'])
@authorize
def metadata_variables():
    variables = None
    wintx_instance = getWintxInstance()
    try:
        variables = wintx_instance.getVariables()
    except WintxError, err:
        return (
         jsonify({'error': err.message}), 200)

    return (
     jsonify({'variables': variables}), 200)


@app.route('/metadata/levels', methods=['GET'])
@authorize
def metadata_levels():
    levels = []
    wintx_instance = getWintxInstance()
    try:
        levels = wintx_instance.getLevels()
    except WintxError, err:
        return (
         jsonify({'error': err.message}), 500)

    return (
     jsonify({'levels': levels}), 200)


@app.route('/metadata/corners', methods=['GET'])
@authorize
def metadata_corners():
    corners = None
    wintx_instance = getWintxInstance()
    try:
        corners = wintx_instance.getLocationCorners()
    except WintxError, err:
        return (
         jsonify({'error': err.message}), 200)

    return (
     jsonify(corners), 200)


@app.route('/database/stats', methods=['GET'])
@authorize
def database_stats():
    stats = None
    wintx_instance = getWintxInstance()
    try:
        stats = wintx_instance.getDatabaseStats()
    except WintxError, err:
        return (
         jsonify({'error': err.message}), 500)

    return (
     jsonify(stats), 200)


if __name__ == '__main__':
    app.run(use_debugger=useDebugger, use_reloader=useReloader, host='0.0.0.0')