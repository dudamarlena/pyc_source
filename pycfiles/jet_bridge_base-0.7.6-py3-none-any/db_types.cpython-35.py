# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/utils/db_types.py
# Compiled at: 2019-11-06 08:08:25
# Size of source mod 2**32: 1217 bytes
from jet_bridge_base.models import data_types
from sqlalchemy.sql import sqltypes
map_data_types = [
 {'query': sqltypes.VARCHAR, 'date_type': data_types.TEXT},
 {'query': sqltypes.TEXT, 'date_type': data_types.TEXT},
 {'query': sqltypes.BOOLEAN, 'date_type': data_types.BOOLEAN},
 {'query': sqltypes.INTEGER, 'date_type': data_types.INTEGER},
 {'query': sqltypes.SMALLINT, 'date_type': data_types.INTEGER},
 {'query': sqltypes.BIGINT, 'date_type': data_types.INTEGER},
 {'query': sqltypes.NUMERIC, 'date_type': data_types.FLOAT},
 {'query': sqltypes.DATETIME, 'date_type': data_types.DATE_TIME},
 {'query': sqltypes.TIMESTAMP, 'date_type': data_types.DATE_TIME},
 {'query': sqltypes.JSON, 'date_type': data_types.JSON}]
default_data_type = data_types.TEXT
try:
    from geoalchemy2 import types
    map_data_types.append({'query': types.Geometry, 'date_type': data_types.GEOMETRY})
    map_data_types.append({'query': types.Geography, 'date_type': data_types.GEOGRAPHY})
except ImportError:
    pass

def map_data_type(value):
    for rule in reversed(map_data_types):
        if isinstance(value, rule['query']):
            return rule['date_type']

    return default_data_type