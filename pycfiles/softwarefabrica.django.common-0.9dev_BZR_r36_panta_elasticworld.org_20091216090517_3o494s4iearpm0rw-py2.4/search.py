# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/common/search.py
# Compiled at: 2009-01-29 07:50:04
from django.db import models
from django.db.models.options import Options
from softwarefabrica.django.utils import usearch

def search_model(query_string, model, fields):
    """
    Perform the requested search (terms in ``query_string``) in the
    specified ``model`` using the specified ``fields``.
    """
    assert issubclass(model, models.Model)
    opts = model._meta
    assert isinstance(opts, Options)
    query = usearch.get_query(query_string, fields)
    if query is not None:
        return model._default_manager.filter(query)
    return model._default_manager.all()


def search_models(query_string, models_and_fields):
    """
    Perform the requested search (terms in ``query_string``) in the models and
    fields specified in ``models_and_fields``.
    ``models_and_fields`` is a list of tuples (MODEL, FIELDS).
    """
    found_objects = []
    found = {}
    for model_fields in models_and_fields:
        (model, fields) = model_fields
        assert issubclass(model, models.Model)
        opts = model._meta
        assert isinstance(opts, Options)
        query = usearch.get_query(query_string, fields)
        found_for_model = []
        if query is not None:
            found_for_model = model._default_manager.filter(query)
        else:
            found_for_model = model._default_manager.all()
        found[opts.verbose_name] = found_for_model
        found_objects.append(dict(model=model, name=opts.verbose_name, name_plural=opts.verbose_name_plural, opts=opts, objects=found_for_model, query_string=query_string))

    return found_objects


def search_queryset(queryset, query_string, fields, model=None):
    """
    Perform the requested search (terms in ``query_string``) filtering the
    specified ``queryset`` using the specified ``fields``.

    Returns the filtered queryset.
    """
    from django.db.models.query import QuerySet
    assert isinstance(queryset, QuerySet)
    queryset = queryset._clone()
    model = model or queryset.model
    assert issubclass(model, models.Model)
    opts = model._meta
    assert isinstance(opts, Options)
    query = usearch.get_query(query_string, fields)
    if query is not None:
        return queryset.filter(query)
    return queryset