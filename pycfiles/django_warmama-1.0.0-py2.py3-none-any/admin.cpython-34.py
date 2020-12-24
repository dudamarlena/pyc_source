# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/mgxrace/django-warmama/warmama/admin.py
# Compiled at: 2015-05-16 14:08:54
# Size of source mod 2**32: 185 bytes
from django.apps import apps
from django.contrib import admin
warmama = apps.get_app_config('warmama')
for model_name, model in warmama.models.items():
    admin.site.register(model)