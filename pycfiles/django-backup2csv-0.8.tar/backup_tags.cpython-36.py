# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmandrille/Secundario/Dropbox/GitLab/escrutinio/escrutinio/backups/templatetags/backup_tags.py
# Compiled at: 2019-06-02 21:43:16
# Size of source mod 2**32: 432 bytes
from django import template
from django.apps import apps
register = template.Library()

@register.simple_tag
def get_modelos(app):
    models = []
    for x in apps.all_models:
        if x == app:
            for y in apps.all_models[x]:
                if apps.all_models[x][y]._meta.auto_created is False:
                    models.append(y)

    return models