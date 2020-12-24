# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucio/Projects/django-custard/custard/custard/conf.py
# Compiled at: 2015-04-01 03:54:55
from __future__ import unicode_literals
import sys
from django.conf import settings as django_settings
from django.utils.functional import cached_property as settings_property
if b'test' in sys.argv:
    settings_property = property
CUSTOM_TYPE_TEXT = b'text'
CUSTOM_TYPE_INTEGER = b'integer'
CUSTOM_TYPE_FLOAT = b'float'
CUSTOM_TYPE_TIME = b'time'
CUSTOM_TYPE_DATE = b'date'
CUSTOM_TYPE_DATETIME = b'datetime'
CUSTOM_TYPE_BOOLEAN = b'boolean'

class LazySettingsDict(object):

    @settings_property
    def CUSTOM_CONTENT_TYPES(self):
        return getattr(django_settings, b'CUSTOM_CONTENT_TYPES', None)

    @settings_property
    def CUSTOM_FIELD_TYPES(self):
        return dict({CUSTOM_TYPE_TEXT: b'django.forms.fields.CharField', 
           CUSTOM_TYPE_INTEGER: b'django.forms.fields.IntegerField', 
           CUSTOM_TYPE_FLOAT: b'django.forms.fields.FloatField', 
           CUSTOM_TYPE_TIME: b'django.forms.fields.TimeField', 
           CUSTOM_TYPE_DATE: b'django.forms.fields.DateField', 
           CUSTOM_TYPE_DATETIME: b'django.forms.fields.DateTimeField', 
           CUSTOM_TYPE_BOOLEAN: b'django.forms.fields.BooleanField'}, **getattr(django_settings, b'CUSTOM_FIELD_TYPES', {}))

    @settings_property
    def CUSTOM_WIDGET_TYPES(self):
        return dict({CUSTOM_TYPE_TEXT: b'django.contrib.admin.widgets.AdminTextInputWidget', 
           CUSTOM_TYPE_INTEGER: b'django.contrib.admin.widgets.AdminIntegerFieldWidget', 
           CUSTOM_TYPE_FLOAT: b'django.contrib.admin.widgets.AdminIntegerFieldWidget', 
           CUSTOM_TYPE_TIME: b'django.contrib.admin.widgets.AdminTimeWidget', 
           CUSTOM_TYPE_DATE: b'django.contrib.admin.widgets.AdminDateWidget', 
           CUSTOM_TYPE_DATETIME: b'django.contrib.admin.widgets.AdminSplitDateTime', 
           CUSTOM_TYPE_BOOLEAN: b'django.forms.widgets.CheckboxInput'}, **getattr(django_settings, b'CUSTOM_WIDGET_TYPES', {}))


settings = LazySettingsDict()