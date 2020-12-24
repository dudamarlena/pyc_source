# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/models.py
# Compiled at: 2017-01-07 15:23:21
# Size of source mod 2**32: 2454 bytes
"""
Module contains basic model class.
"""
import operator, peewee
from tcrudge.utils.schema import Schema

class BaseModel(peewee.Model):
    __doc__ = '\n    Basic abstract ORM model.\n    '

    async def _update(self, app, data):
        """
        By default method sets all given attributes.

        :returns: updated self instance.
        """
        for k, v in data.items():
            setattr(self, k, v)

        await app.objects.update(self)
        return self

    @classmethod
    async def _create(cls, app, data):
        """
        By default method creates instance with all given attributes.

        :returns: created object.
        """
        return await app.objects.create(cls, **data)

    async def _delete(self, app):
        """
        By default model deletion is not allowed.
        """
        raise AttributeError

    @classmethod
    def to_schema(cls, excluded=None):
        """
        Generates JSON schema from ORM model. User can exclude some fields
        from serialization, by default the only fields to exclude are
        pagination settings.

        :param excluded: Excluded parameters.
        :type excluded: list or tuple.
        :return: JSON schema.
        :rtype: dict.
        """
        if not excluded:
            excluded = []
        schema = Schema.create_default_schema()
        excluded += getattr(cls._meta, 'excluded', [])
        for field, type_field in cls._meta.fields.items():
            if field not in excluded:
                schema.add_object({field: type_field.get_column_type()})
                if not type_field.null:
                    schema.add_schema({'required': [field]})
                else:
                    schema.add_object({field: None})

        return schema.to_dict()


FILTER_MAP = {'lt': operator.lt, 
 'gt': operator.gt, 
 'lte': operator.le, 
 'gte': operator.ge, 
 'ne': operator.ne, 
 'like': operator.mod, 
 'ilike': operator.pow, 
 'in': operator.lshift, 
 'isnull': operator.rshift}