# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/queries.py
# Compiled at: 2016-02-24 05:04:05
from __future__ import print_function, unicode_literals
from django.core.cache import cache
from cmstemplates import models as m

def active_templates_for_group(group):
    return list(group.templates.active().order_by(b'weight'))


def get_template_group(name, description=b''):
    group, _ = m.TemplateGroup.objects.get_or_create(name=name, defaults={b'description': description})
    return group


def get_content_for_group(group):
    templates = active_templates_for_group(group)
    content = []
    for template in templates:
        content.append(template.render())

    return (b'').join(content)


def get_cached_content_for_group(group):
    content = cache.get(group.cache_key)
    if content is not None:
        return content
    else:
        content = get_content_for_group(group)
        cache.set(group.cache_key, content)
        return content