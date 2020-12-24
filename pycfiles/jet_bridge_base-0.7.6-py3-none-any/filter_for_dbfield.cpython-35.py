# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/filters/filter_for_dbfield.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 3907 bytes
from sqlalchemy.sql import sqltypes
from jet_bridge_base.filters import lookups
from jet_bridge_base.filters.boolean_filter import BooleanFilter
from jet_bridge_base.filters.char_filter import CharFilter
from jet_bridge_base.filters.datetime_filter import DateTimeFilter
from jet_bridge_base.filters.wkt_filter import WKTFilter
from jet_bridge_base.filters.integer_filter import IntegerFilter
number_lookups = [
 lookups.EXACT,
 lookups.GT,
 lookups.GTE,
 lookups.LT,
 lookups.LTE,
 lookups.ICONTAINS,
 lookups.IN,
 lookups.IS_NULL]
datetime_lookups = [
 lookups.EXACT,
 lookups.GT,
 lookups.GTE,
 lookups.LT,
 lookups.LTE,
 lookups.ICONTAINS,
 lookups.IN,
 lookups.IS_NULL]
text_lookups = [
 lookups.EXACT,
 lookups.ICONTAINS,
 lookups.IN,
 lookups.STARTS_WITH,
 lookups.ENDS_WITH,
 lookups.IS_NULL]
boolean_lookups = [
 lookups.EXACT,
 lookups.IN,
 lookups.IS_NULL]
json_lookups = [
 lookups.JSON_ICONTAINS,
 lookups.IS_NULL]
geography_lookups = [
 lookups.COVEREDBY]
FILTER_FOR_DBFIELD = {sqltypes.VARCHAR: {'filter_class': CharFilter, 'lookups': text_lookups}, 
 sqltypes.TEXT: {'filter_class': CharFilter, 'lookups': text_lookups}, 
 sqltypes.BOOLEAN: {'filter_class': BooleanFilter, 'lookups': boolean_lookups}, 
 sqltypes.INTEGER: {'filter_class': IntegerFilter, 'lookups': number_lookups}, 
 sqltypes.SMALLINT: {'filter_class': IntegerFilter, 'lookups': number_lookups}, 
 sqltypes.NUMERIC: {'filter_class': IntegerFilter, 'lookups': number_lookups}, 
 sqltypes.DATETIME: {'filter_class': DateTimeFilter, 'lookups': datetime_lookups}, 
 sqltypes.TIMESTAMP: {'filter_class': DateTimeFilter, 'lookups': datetime_lookups}, 
 sqltypes.JSON: {'filter_class': CharFilter, 'lookups': json_lookups}}
FILTER_FOR_DBFIELD_DEFAULT = FILTER_FOR_DBFIELD[sqltypes.VARCHAR]
try:
    from geoalchemy2 import types
    FILTER_FOR_DBFIELD[types.Geometry] = {'filter_class': WKTFilter, 'lookups': geography_lookups}
    FILTER_FOR_DBFIELD[types.Geography] = {'filter_class': WKTFilter, 'lookups': geography_lookups}
except ImportError:
    pass

def filter_for_data_type(value):
    for date_type, filter_data in FILTER_FOR_DBFIELD.items():
        if isinstance(value, date_type):
            return filter_data

    return FILTER_FOR_DBFIELD_DEFAULT