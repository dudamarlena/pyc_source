# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/South/south/introspection_plugins/geodjango.py
# Compiled at: 2018-07-11 18:15:31
"""
GeoDjango introspection rules
"""
import django
from django.conf import settings
from south.modelsinspector import add_introspection_rules
has_gis = 'django.contrib.gis' in settings.INSTALLED_APPS
if has_gis:
    from django.contrib.gis.db.models.fields import GeometryField
    if django.VERSION[0] == 1 and django.VERSION[1] >= 1:
        rules = [
         (
          (
           GeometryField,), [],
          {'srid': [
                    'srid', {'default': 4326}], 
             'spatial_index': [
                             'spatial_index', {'default': True}], 
             'dim': [
                   'dim', {'default': 2}], 
             'geography': [
                         'geography', {'default': False}]})]
    else:
        rules = [
         (
          (
           GeometryField,), [],
          {'srid': [
                    '_srid', {'default': 4326}], 
             'spatial_index': [
                             '_index', {'default': True}], 
             'dim': [
                   '_dim', {'default': 2}]})]
    add_introspection_rules(rules, ['^django\\.contrib\\.gis'])