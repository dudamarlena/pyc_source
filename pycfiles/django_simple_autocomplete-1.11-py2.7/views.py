# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_autocomplete/views.py
# Compiled at: 2016-11-08 09:30:37
import pickle, json
from django.http import HttpResponse
from django.db.models.query import QuerySet
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.utils import get_search_fieldname, get_setting

def get_json(request, token):
    """Return matching results as JSON"""
    result = []
    searchtext = request.GET['q']
    if len(searchtext) >= 3:
        pickled = _simple_autocomplete_queryset_cache.get(token, None)
        if pickled is not None:
            app_label, model_name, query = pickle.loads(pickled)
            model = apps.get_model(app_label, model_name)
            queryset = QuerySet(model=model, query=query)
            fieldname = get_search_fieldname(model)
            di = {'%s__istartswith' % fieldname: searchtext}
            app_label_model = '%s.%s' % (app_label, model_name)
            max_items = get_setting(app_label_model, 'max_items', 10)
            items = queryset.filter(**di).order_by(fieldname)[:max_items]
            counts = {}
            for item in items:
                key = unicode(item)
                counts.setdefault(key, 0)
                counts[key] += 1

            for item in items:
                key = value = unicode(item)
                value = getattr(item, fieldname)
                if counts[key] > 1:
                    func = get_setting(app_label_model, 'duplicate_format_function', lambda obj, model, content_type: content_type.name)
                    content_type = ContentType.objects.get_for_model(model)
                    value = '%s (%s)' % (value, func(item, model, content_type))
                result.append((item.id, value))

        else:
            result = 'CACHE_MISS'
    return HttpResponse(json.dumps(result))