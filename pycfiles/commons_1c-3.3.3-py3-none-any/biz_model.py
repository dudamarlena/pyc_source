# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/commonslib/biz_model.py
# Compiled at: 2015-04-04 05:19:06
import inspect
from datetime import datetime
from datetime import date
__author__ = 'freeway'

class Attribute(object):

    def __init__(self, default=None, attri_type=None, datetime_fmt='%Y-%m-%d %H:%M:%S', date_fmt='%Y-%m-%d'):
        super(Attribute, self).__init__()
        self.default = default
        self.datetime_fmt = datetime_fmt
        self.date_fmt = date_fmt
        self.attri_type = attri_type


class BizModel(object):
    _class_attributes = None

    def __init__(self, **kwargs):
        super(BizModel, self).__init__()
        if self.__class__._class_attributes is None:
            self.__class__._class_attributes = get_user_attributes(self.__class__)
        for name, obj in self.__class__._class_attributes:
            if isinstance(obj, Attribute):
                setattr(self, name, self.value_converter(obj, kwargs[name]) if name in kwargs else obj.default)

        return

    @staticmethod
    def value_converter(attribute, val):
        vt = type(val)
        v = val
        if attribute.attri_type is not None and attribute.attri_type != str:
            if val is None:
                v = attribute.default
            elif attribute.attri_type == unicode:
                if vt != unicode:
                    v = str(val).encode('utf-8')
            elif attribute.attri_type == datetime:
                if vt == str or vt == unicode:
                    if len(val.strip()) > 0:
                        v = datetime.strptime(val, attribute.datetime_fmt)
                    else:
                        v = None
            elif attribute.attri_type == date:
                if vt == str or vt == unicode:
                    if len(val.strip()) > 0:
                        v = datetime.strptime(val, attribute.date_fmt).date()
                    else:
                        v = None
            else:
                v = attribute.attri_type(val)
        return v

    def update(self, **kwargs):
        for name, obj in self.__class__._class_attributes:
            if isinstance(obj, Attribute) and name in kwargs:
                setattr(self, name, self.value_converter(obj, kwargs[name]))

        return self

    @property
    def attributes(self):
        d = dict()
        for name, obj in self.__class__._class_attributes:
            if isinstance(obj, Attribute):
                d[name] = getattr(self, name)

        return d


def get_user_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return [ item for item in inspect.getmembers(cls) if item[0] not in boring
           ]