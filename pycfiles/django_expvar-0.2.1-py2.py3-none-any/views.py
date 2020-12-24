# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/anders/code/python/django-expvar/expvar/views.py
# Compiled at: 2016-05-04 16:34:06
import importlib, inspect, json
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import View
from . import ExpVar

def run_single_class(name, obj):
    if not issubclass(obj, ExpVar):
        return []
    if name == 'ExpVar':
        return []
    c = obj()
    name = c.get_name()
    value = c.value()
    evars = []
    if isinstance(value, dict):
        for k, v in value.items():
            evars.append(([name, k], v))

    else:
        evars = [
         (
          [
           name], value)]
    return evars


def insert_nested_key(keys, value, d):
    current = d
    for k in keys[:-1]:
        if k in current:
            current = current[k]
        else:
            current[k] = dict()
            current = current[k]

    current[keys[(-1)]] = value
    return d


def load_expvars_from_app(app):
    d = []
    a = None
    try:
        a = importlib.import_module(('{}.vars').format(app))
    except ImportError:
        pass

    if a is not None:
        for name, obj in inspect.getmembers(a, inspect.isclass):
            d.extend(run_single_class(name, obj))

    return d


class ExpVarView(View):

    def get(self, request):
        d = dict()
        skip = []
        if hasattr(settings, 'EXPVAR_SKIP'):
            skip = settings.EXPVAR_SKIP
        for app in settings.INSTALLED_APPS:
            if app in skip:
                continue
            appvars = load_expvars_from_app(app)
            for keys, v in appvars:
                d = insert_nested_key(keys, v, d)

        return HttpResponse(json.dumps(d), content_type='application/json')