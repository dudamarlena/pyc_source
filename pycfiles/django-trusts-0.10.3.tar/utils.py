# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/thomas/Dev/Project/django-trusts/trusts/utils.py
# Compiled at: 2016-04-29 17:59:15
from __future__ import unicode_literals
import six
from django.db.models import Model

def get_short_model_name_lower(klass):
    if isinstance(klass, six.string_types):
        return klass.lower()
    if issubclass(klass, Model):
        return b'%s.%s' % (klass._meta.app_label.lower(), klass._meta.model_name)
    return b''


def get_short_model_name(klass):
    if isinstance(klass, six.string_types):
        return klass
    if issubclass(klass, Model):
        return b'%s.%s' % (klass._meta.app_label, klass._meta.object_name)
    return b''


def parse_perm_code(perm):
    applabel, action_modelname_permcode = perm.split(b'.', 1)
    action, modelname_permcode = action_modelname_permcode.rsplit(b'_', 1)
    modelname, sep, cond = modelname_permcode.partition(b':')
    return (
     applabel, modelname, action, cond)