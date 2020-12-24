# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmandrille/Secundario/Dropbox/GitLab/escrutinio/escrutinio/backups/functions.py
# Compiled at: 2019-06-03 00:48:50
# Size of source mod 2**32: 660 bytes
from django.db import models
from django.core.cache import cache

def get_fields(clase):
    lista = []
    for field in clase._meta.fields:
        if field.is_relation:
            lista.append((field.name, 'ForeingKey', field.get_internal_type(), field.related_model._meta.model_name))
        else:
            lista.append((field.name, 'RegularField', field.get_internal_type()))

    for field in clase._meta.many_to_many:
        lista.append((field.name, 'ManyToMany', field.get_internal_type(), field.related_model._meta.model_name))

    return lista


models.fields