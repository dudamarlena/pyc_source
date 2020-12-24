# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/FlatDict2.py
# Compiled at: 2017-04-23 10:30:41
from cloudmesh_client.common.FlatDict import FlatDict
import six

class FlatDict2(object):
    if six.PY2:
        primitive = (
         int, str, bool, unicode, dict, list)
    elif six.PY3:
        primitive = (
         int, str, bool, str, bytes, dict, list)

    @classmethod
    def is_primitive(cls, thing):
        return type(thing) in cls.primitive

    @classmethod
    def convert(cls, obj, flatten=True):
        """
            This function converts object into a Dict optionally Flattening it
            :param obj: Object to be converted
            :param flatten: boolean to specify if the dict has to be flattened
            :return dict: the dict of the object (Flattened or Un-flattened)
        """
        dict_result = cls.object_to_dict(obj)
        if flatten:
            dict_result = FlatDict(dict_result)
        return dict_result

    @classmethod
    def object_to_dict(cls, obj):
        """
            This function converts Objects into Dictionary
        """
        dict_obj = dict()
        if obj is not None:
            if type(obj) == list:
                dict_list = []
                for inst in obj:
                    dict_list.append(cls.object_to_dict(inst))

                dict_obj['list'] = dict_list
            elif not cls.is_primitive(obj):
                for key in obj.__dict__:
                    if type(obj.__dict__[key]) == list:
                        dict_list = []
                        for inst in obj.__dict__[key]:
                            dict_list.append(cls.object_to_dict(inst))

                        dict_obj[key] = dict_list
                    elif not cls.is_primitive(obj.__dict__[key]):
                        temp_dict = cls.object_to_dict(obj.__dict__[key])
                        dict_obj[key] = temp_dict
                    else:
                        dict_obj[key] = obj.__dict__[key]

            elif cls.is_primitive(obj):
                return obj
        return dict_obj