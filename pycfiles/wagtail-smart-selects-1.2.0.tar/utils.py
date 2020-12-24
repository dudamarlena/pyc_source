# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rmartins/Desenvolvimento/Django/Apps/wagtaildemo/smart_selects/utils.py
# Compiled at: 2016-01-06 07:19:32
from django.utils.encoding import force_text
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

def unicode_sorter(input):
    """ This function implements sort keys for the german language according to
    DIN 5007."""
    key1 = input.lower()
    key1 = key1.replace('ä', 'a')
    key1 = key1.replace('ö', 'o')
    key1 = key1.replace('ü', 'u')
    key1 = key1.replace('ß', 'ss')
    return key1


def get_limit_choices_to(app_name, model_name, field_name):
    try:
        model = get_model(app_name, model_name)
        field = model._meta.get_field_by_name(field_name)[0]
        limit_choices_to = field.rel.limit_choices_to
    except Exception as e:
        limit_choices_to = None

    return limit_choices_to


def get_queryset(model_class, manager=None, limit_choices_to=None):
    if manager is not None and hasattr(model_class, manager):
        queryset = getattr(model_class, manager)
    else:
        queryset = model_class._default_manager
    if limit_choices_to:
        queryset = queryset.complex_filter(limit_choices_to)
    return queryset


def serialize_results(results):
    return [ {'value': item.pk, 'display': force_text(item)} for item in results ]


def get_keywords(field, value, m2m=False):
    if value == '0':
        keywords = {str('%s__isnull' % field): True}
    elif m2m:
        keywords = {str('%s__pk' % field): str(value)}
    else:
        keywords = {str(field): str(value)}
    return keywords


def sort_results(results):
    """Performs in-place sort of filterchain results."""
    results.sort(key=lambda x: unicode_sorter(force_text(x)))