# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-odnoklassniki-api/odnoklassniki_api/utils.py
# Compiled at: 2015-02-03 23:25:35
from django.core.exceptions import ImproperlyConfigured

def get_improperly_configured_field(app_name, decorate_property=False):

    def field(self):
        raise ImproperlyConfigured("Application '%s' not in INSTALLED_APPS" % app_name)

    if decorate_property:
        field = property(field)
    return field