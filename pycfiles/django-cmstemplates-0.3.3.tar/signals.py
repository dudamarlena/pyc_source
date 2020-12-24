# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/asyncee/git/django-cmstemplates/cmstemplates/signals.py
# Compiled at: 2016-02-24 04:35:30
from __future__ import print_function, unicode_literals
from django.core.cache import cache
from django.db.models import signals
from cmstemplates import models as m

def delete_templategroup_cache(sender, instance, **kwargs):
    cache.delete(instance.cache_key)


def delete_template_templategroup_cache(sender, instance, **kwargs):
    cache.delete(instance.group.cache_key)


signals.post_delete.connect(delete_templategroup_cache, sender=m.TemplateGroup, dispatch_uid=b'delete_templategroup_cache_post_delete')
signals.post_delete.connect(delete_template_templategroup_cache, sender=m.Template, dispatch_uid=b'delete_template_templategroup_cache_post_delete')
signals.post_save.connect(delete_templategroup_cache, sender=m.TemplateGroup, dispatch_uid=b'delete_templategroup_cache_post_save')
signals.post_save.connect(delete_template_templategroup_cache, sender=m.Template, dispatch_uid=b'delete_template_templategroup_cache_post_save')