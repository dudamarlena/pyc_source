# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skywisemodel/_timeseries.py
# Compiled at: 2017-05-19 14:29:52
from voluptuous import Any, Schema
from . import ModelApiResource
from ._validation import datetime, datetime_to_str

class TimeSeries(ModelApiResource):
    _path = '/variables/{variable_id}/timeseries/{lat}/{lon}'
    _deserialize = Schema({'series': [
                {'validTime': datetime, 
                   'value': Any(None, float)}], 
       'maximum': {'validTime': datetime, 
                   'value': Any(None, float)}, 
       'minimum': {'validTime': datetime, 
                   'value': Any(None, float)}, 
       'mean': Any(None, float), 
       'median': Any(None, float), 
       'mode': Any(None, float), 
       'unit': {'description': Any(str, unicode), 
                'label': Any(str, unicode)}})
    _serialize = Schema({'series': [
                {'validTime': datetime_to_str, 
                   'value': Any(None, float)}], 
       'maximum': {'validTime': datetime_to_str, 
                   'value': Any(None, float)}, 
       'minimum': {'validTime': datetime_to_str, 
                   'value': Any(None, float)}, 
       'mean': Any(None, float), 
       'median': Any(None, float), 
       'mode': Any(None, float), 
       'unit': {'description': Any(str, unicode), 
                'label': Any(str, unicode)}})