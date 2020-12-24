# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/contenttypes/checks.py
# Compiled at: 2019-02-14 00:35:15
from __future__ import unicode_literals
from itertools import chain
from django.apps import apps
from django.utils import six

def check_generic_foreign_keys(app_configs=None, **kwargs):
    from .fields import GenericForeignKey
    if app_configs is None:
        models = apps.get_models()
    else:
        models = chain.from_iterable(app_config.get_models() for app_config in app_configs)
    errors = []
    fields = (obj for model in models for obj in six.itervalues(vars(model)) if isinstance(obj, GenericForeignKey))
    for field in fields:
        errors.extend(field.check())

    return errors