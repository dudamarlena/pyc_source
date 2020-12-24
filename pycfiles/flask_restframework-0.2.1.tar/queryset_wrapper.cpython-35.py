# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/queryset_wrapper.py
# Compiled at: 2017-10-27 10:49:50
# Size of source mod 2**32: 7423 bytes
import copy
from mongoengine.base.document import BaseDocument
from mongoengine.document import Document
from mongoengine.queryset.queryset import QuerySet
from pymongo.cursor import Cursor

class InstanceWrapper(object):
    __doc__ = '\n    Обертка для записи из базы.\n\n    Поддерживается Mongoengine Document и dict из курсора.\n\n    '

    def __init__(self, item):
        self.item = item

    def get_id(self):
        """
        Возвращает id записи
        """
        raise NotImplementedError

    def get_field(self, key):
        """
        Возвращает значение поля key для обернутой записи.
        Должен поддерживать __ Django нотацию
        """
        raise NotImplementedError

    def update(self, validated_data):
        raise NotImplementedError

    def to_dict(self):
        """
        Should return dict representation of instance
        """
        raise NotImplementedError

    def delete(self):
        """
        Should delete this instance
        """
        raise NotImplementedError

    @classmethod
    def from_instance(cls, item):
        """
        Returns wrapped instance
        """
        if isinstance(item, Document):
            return MongoInstanceWrapper(item)
        if isinstance(item, dict):
            return CursorInstanceWrapper(item)
        raise TypeError('Incorrect type {}'.format(type(item)))


class MongoInstanceWrapper(InstanceWrapper):
    __doc__ = '\n    Обертка для Mongoengine Document записи\n    '
    item = None

    def delete(self):
        self.item.delete()

    def to_dict(self):
        return self.item.to_mongo()

    def get_id(self):
        return self.item.pk

    def update(self, validated_data):
        for key, value in validated_data.items():
            setattr(self.item, key, value)

        self.item.save()

    def get_field(self, key):
        out = self.item
        for part in key.split('__'):
            try:
                out = getattr(out, part)
            except:
                return

        if isinstance(out, (BaseDocument, dict)):
            return MongoInstanceWrapper(out)
        if isinstance(out, list):
            r = []
            for item in out:
                if isinstance(item, (BaseDocument, dict)):
                    r.append(MongoInstanceWrapper(item))
                else:
                    r.append(item)

            return r
        return out


class CursorInstanceWrapper(InstanceWrapper):
    __doc__ = '\n    Обертка для записи из pymongo.Cursor (по сути обычный dict)\n    '

    def to_dict(self):
        return dict(self.item)

    def get_id(self):
        return self.item['_id']

    def get_field(self, key):
        if key == 'id':
            key = '_id'
        out = self.item
        for part in key.split('__'):
            try:
                out = out.get(part)
            except:
                return

        if isinstance(out, dict):
            return CursorInstanceWrapper(out)
        if isinstance(out, list):
            r = []
            for item in out:
                if isinstance(item, dict):
                    r.append(CursorInstanceWrapper(item))
                else:
                    r.append(item)

            return r
        return out


class QuerysetWrapper(object):
    __doc__ = '\n    Обертка для Queryset.\n    '

    def __init__(self, data, wrapperType):
        self.wrapperType = wrapperType
        self.data = data

    @classmethod
    def from_queryset(cls, qs):
        """
        Returns wrapped queryset from passed qs
        """
        if isinstance(qs, QuerySet):
            return MongoDbQuerySet(qs, MongoInstanceWrapper)
        if isinstance(qs, (Cursor, list)):
            return CursorQuerySet(qs, CursorInstanceWrapper)
        if callable(qs):
            return cls.from_queryset(qs())
        if isinstance(qs, QuerysetWrapper):
            return qs
        raise TypeError('Unknown type {}'.format(type(qs)))

    def get(self, id):
        """Should return one instance by it id"""
        raise NotImplementedError

    def get_data(self):
        """
        Returns iterable of InstanceWrapper
        """
        for item in self.data:
            yield self.wrapperType(item)

    def count(self):
        """
        Should return total count of items in QuerySet
        """
        raise NotImplementedError

    def slice(self, frm, to):
        """
        Should slice queryset
        """
        raise NotImplementedError

    def filter_by(self, **filters):
        """
        Should filter queryset by filters (Django style filtering)
        Returns new queryset
        """
        raise NotImplementedError

    def order_by(self, *ordering):
        """
        Should return ordered queryset.

        :param ordering: list of fields: "field" for ASC, "-field" for DESC
        """
        raise NotImplementedError


class MongoDbQuerySet(QuerysetWrapper):
    __doc__ = '\n    Обертка для MongoEngine Queryset\n    '

    def order_by(self, *ordering):
        return MongoDbQuerySet(self.data.order_by(*ordering), self.wrapperType)

    def filter_by(self, **filters):
        return MongoDbQuerySet(self.data.filter(**filters), self.wrapperType)

    def slice(self, frm, to):
        return MongoDbQuerySet(self.data[frm:to], self.wrapperType)

    def get(self, id):
        return self.wrapperType(self.data.get(id=id))

    def count(self):
        return self.data.count()


class CursorQuerySet(QuerysetWrapper):
    __doc__ = '\n    Обертка для pymongo.Cursor\n    '

    def __init__(self, *a, **k):
        super(CursorQuerySet, self).__init__(*a, **k)
        self.data = list(self.data)

    def count(self):
        return len(self.data)

    def filter_by(self, id=None):
        return CursorQuerySet(filter(lambda item: item['_id'] == id, self.data), wrapperType=self.wrapperType)

    def slice(self, frm, to):
        return self.data[frm:to]


class MongoCollectionQuerySet(QuerysetWrapper):
    __doc__ = '\n    Обертка для целой коллекции монги\n    '

    def slice(self, frm, to):
        qs = copy.copy(self)
        qs.frm = frm
        qs.to = to
        return qs

    def count(self):
        return self.collection.find(self.filter_clause).count()

    def filter_by(self, **filters):
        qs = copy.copy(self)
        qs.filter_clause = self._parse_filter_clause(filters)
        return qs

    @property
    def data(self):
        cursor = self.collection.find(self.filter_clause)
        if self.to:
            return cursor[self.frm:self.to]
        return cursor[self.frm]

    def __init__(self, collection):
        self.collection = collection
        self.wrapperType = CursorInstanceWrapper
        self.filter_clause = {}
        self.frm = 0
        self.to = None

    def _parse_filter_clause(self, filters):
        out = {}
        for key, value in filters.items():
            if isinstance(value, list):
                out[key] = value[0]
            else:
                out[key] = value

        return out