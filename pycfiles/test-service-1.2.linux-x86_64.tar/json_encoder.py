# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kylin/pyenvs/kylins-flask/lib/python2.7/site-packages/test_service/json_encoder.py
# Compiled at: 2015-02-14 10:29:51
__author__ = 'kylinfish@126.com'
__date__ = '2014/10/17'
from types import ListType, DictType
from json import dumps
from decimal import Decimal
from django.db.models.query import QuerySet
from django.core.serializers.json import DateTimeAwareJSONEncoder
from django.contrib.gis import geos

def json_data_encode(json_data):
    u"""可以序列化 datetime, QuerySet 等多类型数据.

        :param json_data
    """

    def _any(data):
        if isinstance(data, ListType):
            return_data = _list(data)
        elif isinstance(data, DictType):
            return_data = _dict(data)
        elif isinstance(data, Decimal):
            return_data = str(data)
        elif isinstance(data, QuerySet):
            return_data = _list(data)
        elif isinstance(data, geos.Point):
            return_data = None
        else:
            return_data = data
        return return_data

    def _list(data):
        list_data = []
        for v in data:
            list_data.append(_any(v))

        return list_data

    def _dict(data):
        dict_data = {}
        for k, v in data.items():
            dict_data[k] = _any(v)

        return dict_data

    ret = _any(json_data)
    return dumps(ret, cls=DateTimeAwareJSONEncoder, ensure_ascii=False, indent=4)