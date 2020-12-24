# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/json_utils.py
# Compiled at: 2016-06-11 06:32:43
import json

def dict_to_obj(json_dict_or_list):

    class _obj(dict):

        def __init__(self, d):
            for a, b in d.iteritems():
                setattr(self, a, dict_to_obj(b))

        def to_json(self):
            return json.dumps(self.__dict__)

    if isinstance(json_dict_or_list, (list, tuple)):
        return [ dict_to_obj(x) for x in json_dict_or_list ]
    if isinstance(json_dict_or_list, dict):
        return _obj(json_dict_or_list)
    return json_dict_or_list


def to_obj(msg):
    return dict_to_obj(json.loads(msg))