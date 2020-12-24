# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dbsync/serializers/json.py
# Compiled at: 2015-04-10 05:21:53
__author__ = 'nathan'
import json
from datetime import date, datetime
from dbsync.serializers.base import BaseSerializer

class JSONSerializer(BaseSerializer):
    """ serialize model to json """

    def serialize(self, model, ensure_ascii=True, cls=DatetimeJSONEncoder):
        """

        :param model:
        :param ensure_ascii: boolean, default True, see alse json.dumps()
        :param cls:
        :return:
        """
        return json.dumps(model, ensure_ascii, cls)


class DatetimeJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            if isinstance(obj, date):
                return obj.strftime('%Y-%m-%d')
            return json.JSONEncoder.default(self, obj)