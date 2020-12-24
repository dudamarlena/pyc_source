# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe_table/utils.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 4483 bytes
from typing import Any, Dict, List, Tuple
import django.apps as apps
from django.db import models
from django.db.models import Q
from django.db.models.base import ModelBase
from django.contrib.auth import get_user_model
from .exceptions import TableDoesNotExists
SUPPORTED_FIELDS = (
 models.AutoField,
 models.BigAutoField,
 models.BigIntegerField,
 models.BooleanField,
 models.CharField,
 models.DateField,
 models.DateTimeField,
 models.DecimalField,
 models.EmailField,
 models.FloatField,
 models.ForeignKey,
 models.IntegerField,
 models.GenericIPAddressField,
 models.NullBooleanField,
 models.PositiveIntegerField,
 models.PositiveSmallIntegerField,
 models.SlugField,
 models.SmallIntegerField,
 models.TextField,
 models.TimeField,
 models.URLField,
 models.UUIDField)

def get_model_by_table(table: str) -> ModelBase:
    """
    Returns Django model by table name.
    """
    if table == 'auth_user':
        return get_user_model()
    for app_models in apps.all_models.values():
        for cls in app_models.values():
            if cls._meta.db_table == table:
                return cls

    raise TableDoesNotExists(table)


def get_models_choices() -> Tuple[(Tuple[(str, Tuple[(Tuple[(str, str)], ...)])], ...)]:
    """
    Returns sorted and grouped choices of all models per app.

    Example output:

    .. code-block:: txt

        (
            'app1',
            (
                ('choice1 key', 'choice1 name'),
                ...
            ),
        ), (
            'app2',
            (
                ('choice2 key', 'choice2 name'),
                ...
            ),
        ), (
            ...
        )
    """
    return tuple(((app, tuple(((cls._meta.db_table, cls._meta.object_name) for model, cls in sorted(app_models.items())))) for app, app_models in sorted(apps.all_models.items()) if app_models))


def get_table_choices(table: str) -> Dict[(str, List[Tuple[(str, str, str)]])]:
    """
    Returns choices for table depending on exact table name.

    .. code-block:: txt

        {
            "columns": [
                ["name", "label", "type"],
                ...
            ]
        }
    """
    model = get_model_by_table(table)
    choices = {'columns': [(field.name, getattr(field, 'verbose_name', field.name), get_field_type(field)) for field in model._meta.get_fields() if field.__class__ in SUPPORTED_FIELDS]}
    return choices


def get_field_type(field) -> str:
    if isinstance(field, (models.BooleanField, models.NullBooleanField)):
        return 'boolean'
    if isinstance(field, (models.AutoField, models.IntegerField)):
        return 'integer'
    if isinstance(field, (models.DecimalField, models.FloatField)):
        return 'float'
    return 'string'


def get_filter_params(model, filter_data: Dict[(str, Any)]) -> Tuple[(List[Any], Dict[(str, Any)])]:
    """
    Returns tuple with args and kwargs for queryset filter.
    """
    filter_args = []
    filter_kwds = {}
    for field in model._meta.get_fields():
        if field.name not in filter_data:
            continue
        key = field.name
        value = filter_data[field.name]
        if isinstance(field, models.ForeignKey) and isinstance(value, str):
            foreign_filter = Q()
            for foreign_field in field.rel.model._meta.get_fields():
                if isinstance(foreign_field, (models.CharField, models.TextField)):
                    foreign_filter |= Q(**{'{}__{}__icontains'.format(key, foreign_field.name): value})

            filter_args.append(foreign_filter)
        elif isinstance(field, (models.CharField, models.TextField)):
            filter_kwds['{}__icontains'.format(key)] = value
        else:
            filter_kwds[key] = value

    return (
     filter_args, filter_kwds)