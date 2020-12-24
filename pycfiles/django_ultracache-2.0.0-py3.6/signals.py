# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache/ultracache/signals.py
# Compiled at: 2018-09-10 07:18:29
import threading
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.migrations.recorder import MigrationRecorder
from django.db.models import Model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
try:
    from django.utils.module_loading import import_string as importer
except ImportError:
    from django.utils.module_loading import import_by_path as importer

try:
    purger = importer(settings.ULTRACACHE['purge']['method'])
except (AttributeError, KeyError):
    purger = None

try:
    invalidate = settings.ULTRACACHE['invalidate']
except (AttributeError, KeyError):
    invalidate = True

@receiver(post_save)
def on_post_save(sender, **kwargs):
    """Expire ultracache cache keys affected by this object
    """
    if not invalidate:
        return
    else:
        if kwargs.get('raw', False):
            return
        if sender is MigrationRecorder.Migration:
            return
        if issubclass(sender, Model):
            obj = kwargs['instance']
            if isinstance(obj, Model):
                try:
                    ct = ContentType.objects.get_for_model(sender)
                except RuntimeError:
                    return

                if kwargs.get('created', False):
                    key = 'ucache-ct-%s' % ct.id
                    to_delete = cache.get(key, [])
                    if to_delete:
                        try:
                            cache.delete_many(to_delete)
                        except NotImplementedError:
                            for k in to_delete:
                                cache.delete(k)

                    cache.delete(key)
                    key = 'ucache-ct-pth-%s' % ct.id
                    if purger is not None:
                        for li in cache.get(key, []):
                            purger(li[0], li[1])

                    cache.delete(key)
                else:
                    key = 'ucache-%s-%s' % (ct.id, obj.pk)
                    to_delete = cache.get(key, [])
                    if to_delete:
                        try:
                            cache.delete_many(to_delete)
                        except NotImplementedError:
                            for k in to_delete:
                                cache.delete(k)

                    cache.delete(key)
                    key = 'ucache-pth-%s-%s' % (ct.id, obj.pk)
                    if purger is not None:
                        for li in cache.get(key, []):
                            purger(li[0], li[1])

                    cache.delete(key)
        return


@receiver(post_delete)
def on_post_delete(sender, **kwargs):
    """Expire ultracache cache keys affected by this object
    """
    if not invalidate:
        return
    else:
        if kwargs.get('raw', False):
            return
        if sender is MigrationRecorder.Migration:
            return
        if issubclass(sender, Model):
            obj = kwargs['instance']
            if isinstance(obj, Model):
                try:
                    ct = ContentType.objects.get_for_model(sender)
                except RuntimeError:
                    return

                key = 'ucache-%s-%s' % (ct.id, obj.pk)
                to_delete = cache.get(key, [])
                if to_delete:
                    try:
                        cache.delete_many(to_delete)
                    except NotImplementedError:
                        for k in to_delete:
                            cache.delete(k)

                cache.delete(key)
                key = 'ucache-pth-%s-%s' % (ct.id, obj.pk)
                if purger is not None:
                    for li in cache.get(key, []):
                        purger(li[0], li[1])

                cache.delete(key)
        return