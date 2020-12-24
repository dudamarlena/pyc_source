# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/utils.py
# Compiled at: 2014-08-09 03:47:51
from plugshop import settings
from django.utils.importlib import import_module
from django.core.cache import cache
from django.db.models.loading import get_model as django_get_model

def get_model(path):
    model = django_get_model(*path.split('.'))
    return model


def load_class(path):
    module_path, class_name = path.rsplit('.', 1)
    module = import_module(module_path)
    cl = getattr(module, class_name)
    return cl


def is_default_model(name):
    model = getattr(settings, '%s_MODEL' % name, None)
    default_model = getattr(settings, '%s_MODEL_DEFAULT' % name, None)
    if model and default_model:
        return model == default_model
    else:
        return False
        return


def serialize_model(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_to_string(instance)

    return data


def serialize_queryset(queryset):
    return [ serialize_model(item) for item in queryset ]


def get_categories(*args, **kwargs):
    categories = cache.get('plugshop_categories')
    if categories is None:
        categories = get_model(settings.CATEGORY_MODEL).objects.all()
        cache.set('plugshop_categories', categories)
    return categories