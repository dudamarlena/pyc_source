# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lucaswiman/opensource/django-predicate/predicate/type_inference/field_registry.py
# Compiled at: 2016-04-07 16:29:19
import datetime
from collections import OrderedDict
from decimal import Decimal
import django
from django.db import models
from django.db.models import ManyToManyField
from django.db.models import ManyToManyRel
from django.db.models import ManyToOneRel
from django.db.models import OneToOneRel
from typing import Optional
from typing import TypeVar
from predicate.type_inference.utils import Nullable
from predicate.type_inference.utils import Relation
UKNOWN_TYPE = TypeVar('Unknown')

class _FieldRegistry(OrderedDict):

    def register(self, field_class, field_type):
        self[field_class] = field_type

    def get_type_for_field(self, field):
        """
        Takes an instance of a field and returns the expected type.

        Returns a type variable
        """
        if django.VERSION < (1, 8):
            raise NotImplementedError
        for field_class, inferred_type in reversed(self.items()):
            if isinstance(field, field_class):
                if getattr(field, 'null', False):
                    return Optional[inferred_type]
                else:
                    return inferred_type

        if isinstance(field, (models.OneToOneField, models.ForeignKey)):
            model = field.related.model
            if field.null:
                return Nullable[model]
            return model
        if isinstance(field, OneToOneRel):
            return Nullable[field.to]
        if isinstance(field, (ManyToOneRel, ManyToManyRel)):
            return Relation[field.to]
        if isinstance(field, ManyToManyField):
            return Relation[field.related_model]
        if isinstance(field, models.Field):
            raise NotImplementedError(field)
        return UKNOWN_TYPE


registry = _FieldRegistry([
 (
  models.IntegerField, int),
 (
  models.BigIntegerField, int),
 (
  models.CharField, unicode),
 (
  models.TextField, unicode),
 (
  models.DecimalField, Decimal),
 (
  models.BooleanField, bool),
 (
  models.NullBooleanField, bool),
 (
  models.DateField, datetime.date),
 (
  models.DateTimeField, datetime.datetime)])