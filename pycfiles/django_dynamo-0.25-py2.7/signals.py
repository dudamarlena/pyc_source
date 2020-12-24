# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dynamo\signals.py
# Compiled at: 2011-08-02 15:59:24
import django.dispatch
pre_model_creation = django.dispatch.Signal(providing_args=['new_model'])
post_model_creation = django.dispatch.Signal(providing_args=['new_model'])
pre_model_update = django.dispatch.Signal(providing_args=['old_model', 'new_model'])
post_model_update = django.dispatch.Signal(providing_args=['old_model', 'new_model'])
pre_model_delete = django.dispatch.Signal(providing_args=['old_model'])
post_model_delete = django.dispatch.Signal(providing_args=['old_model'])
pre_field_creation = django.dispatch.Signal(providing_args=['new_field'])
post_field_creation = django.dispatch.Signal(providing_args=['new_field'])
pre_field_update = django.dispatch.Signal(providing_args=['old_field', 'new_field'])
post_field_update = django.dispatch.Signal(providing_args=['old_field', 'new_field'])
pre_field_delete = django.dispatch.Signal(providing_args=['old_field'])
post_field_delete = django.dispatch.Signal(providing_args=['old_field'])