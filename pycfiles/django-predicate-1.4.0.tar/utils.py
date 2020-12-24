# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lucaswiman/opensource/django-predicate/predicate/type_inference/utils.py
# Compiled at: 2016-04-07 16:19:33
from django.db import models
from typing import Container
from typing import Final
from typing import GenericMeta
from typing import List
from typing import TypingMeta
from typing import Union
from typing import _geqv
from typing import _gorg

def is_specialization_of(cls1, cls2):
    """
    Returns True if cls1 is a specialized container of cls2.
    """
    if not (isinstance(cls1, GenericMeta) and isinstance(cls2, GenericMeta)):
        return False
    return _geqv(cls1, cls2) and all(issubclass(param1, param2) for param1, param2 in zip(cls1.__parameters__, cls2.__parameters__))


def generic_isinstance(obj, cls):
    obj_type = type(obj)
    if issubclass(obj_type, cls):
        if isinstance(obj_type, GenericMeta):
            if issubclass(_gorg(obj_type), Container):
                container_type, = obj.__parameters__
                return all(generic_isinstance(container_obj, container_type) for container_obj in obj)
        return True
    return False


class NullType(object):

    def __repr__(self):
        return 'NULL'

    def __nonzero__(self):
        return True


class NullableMeta(TypingMeta):
    """Metaclass for NullableMeta."""

    def __new__(cls, name, bases, namespace):
        cls.assert_no_subclassing(bases)
        return super(NullableMeta, cls).__new__(cls, name, bases, namespace)

    def __getitem__(self, arg):
        if not issubclass(arg, models.Model):
            raise TypeError('NullableMeta[t] requires a Model.')
        ret = Union[(arg, NullType)]
        ret.model = arg
        return ret


class Nullable(Final):
    """
    Type for holding Nullable relations. Based on ``Optional``.

    Nullable[X] is equivalent to Union[X, type(NULL)].
    """
    __metaclass__ = NullableMeta
    __slots__ = ()

    @staticmethod
    def get_model(cls):
        return next(union_type for union_type in cls.__union_params__ if not union_type == NullType)


NULL = NullType()
NullableRelation = Nullable[models.Model]

class Relation(List[models.Model]):
    """
    Type to record Manager and QuerySet classes.
    """

    def __init__(self, manager_or_queryset):
        if not isinstance(manager_or_queryset.model, self.get_model()):
            raise TypeError('%r does not match model type %r' % (manager_or_queryset, self.get_model()))
        super(Relation, self).__init__(manager_or_queryset.all())

    @classmethod
    def get_model(cls):
        if hasattr(cls, '_model'):
            return cls._model
        model_type, = cls.__parameters__
        if issubclass(model_type, NullableRelation):
            model_type = Nullable.get_model(model_type)
        if not issubclass(model_type, models.Model):
            raise TypeError('%r has a non-Model type %r' % (cls, model_type))
        cls._model = model_type
        return model_type