# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/tests/model_coverage.py
# Compiled at: 2009-10-31 23:19:40
from django.db.models.loading import get_models, get_apps

def run():
    for app_mod in get_apps():
        app_models = get_models(app_mod)
        for model in app_models:
            try:
                print model.__module__, model.__name__, model.objects.all().count()
            except Exception, e:
                print e