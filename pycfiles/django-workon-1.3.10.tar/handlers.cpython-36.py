# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DJANGO-WORKON/workon/contrib/cleaner/handlers.py
# Compiled at: 2018-03-04 05:46:43
# Size of source mod 2**32: 3942 bytes
"""
    Signal handlers to manage FileField files.
"""
try:
    from django.db.transaction import on_commit
except ImportError:

    def on_commit(func, using=None):
        func()


from django.db.models.signals import post_init, pre_save, post_save, post_delete
from workon.contrib.cleaner import cache
from workon.contrib.cleaner.signals import cleanup_pre_delete, cleanup_post_delete

class FakeInstance(object):
    __doc__ = 'A Fake model instance to ensure an instance is not modified'


def ensure_delete_ready(instance, field_name, file_):
    """Ensure the file is ready for deletion"""
    file_.instance = FakeInstance()
    model_name = cache.get_model_name(instance)
    if not hasattr(file_, 'field'):
        file_.field = cache.get_field(model_name, field_name)()
        file_.field.name = field_name
    if not hasattr(file_, 'storage'):
        file_.storage = cache.get_field_storage(model_name, field_name)()


def cache_original_post_init(sender, instance, **kwargs):
    """Post_init on all models with file fields, saves original values"""
    cache.make_cleanup_cache(instance)


def fallback_pre_save(sender, instance, raw, update_fields, using, **kwargs):
    """Fallback to the database to remake the cleanup cache if there is none"""
    if raw:
        return
    else:
        if instance.pk:
            if not cache.has_cache(instance):
                try:
                    db_instance = sender.objects.get(pk=(instance.pk))
                except sender.DoesNotExist:
                    return
                else:
                    cache.make_cleanup_cache(instance, source=db_instance)


def delete_old_post_save(sender, instance, raw, created, update_fields, using, **kwargs):
    """Post_save on all models with file fields, deletes old files"""
    if raw or created:
        return
    for field_name, new_file in cache.fields_for_model_instance(instance):
        if update_fields is None or field_name in update_fields:
            old_file = cache.get_field_attr(instance, field_name)
            if old_file != new_file:
                delete_file(instance, field_name, old_file, using)

    cache.make_cleanup_cache(instance)


def delete_all_post_delete(sender, instance, using, **kwargs):
    """Post_delete on all models with file fields, deletes all files"""
    for field_name, file_ in cache.fields_for_model_instance(instance):
        delete_file(instance, field_name, file_, using)


def delete_file(instance, field_name, file_, using):
    """Deletes a file"""
    if not file_ or not file_.name:
        return

    def run_on_commit():
        cleanup_pre_delete.send(sender=None, file=file_)
        file_.delete(save=False)
        cleanup_post_delete.send(sender=None, file=file_)

    ensure_delete_ready(instance, field_name, file_)
    on_commit(run_on_commit, using)


def connect():
    for model in cache.cleanup_models():
        key = '{{}}_django_cleanup_{}'.format(cache.get_model_name(model))
        post_init.connect(cache_original_post_init, sender=model, dispatch_uid=(key.format('post_init')))
        pre_save.connect(fallback_pre_save, sender=model, dispatch_uid=(key.format('pre_save')))
        post_save.connect(delete_old_post_save, sender=model, dispatch_uid=(key.format('post_save')))
        post_delete.connect(delete_all_post_delete, sender=model, dispatch_uid=(key.format('post_delete')))