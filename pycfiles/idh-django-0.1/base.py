# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\formatter\base.py
# Compiled at: 2018-02-12 22:15:16
# Size of source mod 2**32: 3616 bytes
from datetime import datetime
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.db.models.query import QuerySet
from idh.django.utils import load_module

class Formatter(object):

    def content_type(self):
        pass

    def content_data(self, data, **kwargs):
        pass

    def create(name):
        formatter = load_module(name)
        return formatter()

    def fx_dumps(self, data, **kwargs):
        max_deep = 3
        if 'max_deep' in kwargs:
            max_deep = int(kwargs['max_deep'])
        if max_deep < 1:
            max_deep = 1
        alias = {}
        if 'alias' in kwargs:
            alias = kwargs['alias']
        nullable = True
        if 'nullable' in kwargs:
            nullable = kwargs['nullable']
        hidden = {}
        if 'hidden' in kwargs:
            hidden = kwargs['hidden']
        return self.fx_format(data, alias, max_deep, hidden, nullable, 0)

    def fx_format(self, data, alias={}, max_deep=3, hidden={}, nullable=True, deep=0):
        if isinstance(data, models.Model):
            return self.fx_model(data, alias, max_deep, hidden, nullable, deep)
        else:
            if isinstance(data, dict):
                return self.fx_dict(data, alias, max_deep, hidden, nullable)
            if isinstance(data, list):
                return self.fx_list(data, alias, max_deep, hidden, nullable)
            if isinstance(data, QuerySet):
                return self.fx_list(list(data), alias, max_deep, hidden, nullable)
            if hasattr(data, '__dict__'):
                return self.fx_dict(data.__dict__, alias, max_deep, hidden, nullable)
            if isinstance(data, datetime):
                return data.isoformat(' ')
            return data

    def fx_model(self, data, alias={}, max_deep=3, hidden={}, nullable=True, deep=0):
        if deep >= max_deep:
            if hasattr(data, 'pk'):
                return {'pk': data.pk}
            return {}
        fields = data._meta.get_fields()
        result = {}
        for f in fields:
            name = f.name
            if name in hidden:
                pass
            else:
                value = None
                if hasattr(data, name):
                    value = getattr(data, name)
                if name in alias:
                    name = alias[name]
                if value is not None:
                    if issubclass(type(f), ManyToManyField):
                        value = value.all()
                    value = self.fx_format(value, alias, max_deep, hidden, nullable, deep + 1)
                    result[name] = value
                elif nullable:
                    result[name] = value

        return result

    def fx_dict(self, data, alias={}, max_deep=3, hidden={}, nullable=True):
        result = {}
        for key, value in data.items():
            if value is not None:
                value = self.fx_format(value, alias, max_deep, hidden, nullable)
                result[key] = value
            elif nullable:
                result[key] = value

        return result

    def fx_list(self, data, alias={}, max_deep=3, hidden={}, nullable=True):
        result = []
        for value in data:
            if value is not None:
                value = self.fx_format(value, alias, max_deep, hidden, nullable)
                result.append(value)
            elif nullable:
                result.append(value)

        return result