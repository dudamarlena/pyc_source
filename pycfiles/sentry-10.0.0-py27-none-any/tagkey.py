# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/tagstore/v2/models/tagkey.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import, print_function
from django.db import models, router, connections, transaction, IntegrityError
from django.utils.translation import ugettext_lazy as _
from sentry.tagstore import TagKeyStatus
from sentry.tagstore.query import TagStoreManager
from sentry.constants import MAX_TAG_KEY_LENGTH
from sentry.db.models import Model, BoundedPositiveIntegerField, BoundedBigIntegerField, sane_repr
from sentry.utils.cache import cache
from sentry.utils.hashlib import md5_text

class TagKey(Model):
    """
    Stores references to available filters keys.
    """
    __core__ = False
    project_id = BoundedBigIntegerField(db_index=True)
    environment_id = BoundedBigIntegerField()
    key = models.CharField(max_length=MAX_TAG_KEY_LENGTH)
    values_seen = BoundedPositiveIntegerField(default=0)
    status = BoundedPositiveIntegerField(choices=(
     (
      TagKeyStatus.VISIBLE, _('Visible')),
     (
      TagKeyStatus.PENDING_DELETION, _('Pending Deletion')),
     (
      TagKeyStatus.DELETION_IN_PROGRESS, _('Deletion in Progress'))), default=TagKeyStatus.VISIBLE)
    objects = TagStoreManager()

    class Meta:
        app_label = 'tagstore'
        unique_together = (('project_id', 'environment_id', 'key'), )

    __repr__ = sane_repr('project_id', 'environment_id', 'key')

    def delete(self):
        using = router.db_for_read(TagKey)
        cursor = connections[using].cursor()
        cursor.execute('\n            DELETE FROM tagstore_tagkey\n            WHERE project_id = %s\n              AND id = %s\n        ', [
         self.project_id, self.id])

    def get_label(self):
        from sentry import tagstore
        return tagstore.get_tag_key_label(self.key)

    def get_audit_log_data(self):
        return {'key': self.key}

    @classmethod
    def get_cache_key(cls, project_id, environment_id, key):
        return 'tagkey:1:%s:%s:%s' % (project_id, environment_id, md5_text(key).hexdigest())

    @classmethod
    def get_or_create(cls, project_id, environment_id, key, **kwargs):
        cache_key = cls.get_cache_key(project_id, environment_id, key)
        rv = cache.get(cache_key)
        created = False
        if rv is None:
            rv, created = cls.objects.get_or_create(project_id=project_id, environment_id=environment_id, key=key, **kwargs)
            cache.set(cache_key, rv, 3600)
        return (rv, created)

    @classmethod
    def get_or_create_bulk(cls, project_id, environment_id, keys):
        key_to_model = {key:None for key in keys}
        remaining_keys = set(keys)
        cache_key_to_key = {cls.get_cache_key(project_id, environment_id, key):key for key in keys}
        cache_key_to_models = cache.get_many(cache_key_to_key.keys())
        for model in cache_key_to_models.values():
            key_to_model[model.key] = model
            remaining_keys.remove(model.key)

        if not remaining_keys:
            return key_to_model
        to_cache = {}
        for model in cls.objects.filter(project_id=project_id, environment_id=environment_id, key__in=remaining_keys):
            key_to_model[model.key] = to_cache[cls.get_cache_key(project_id, environment_id, model.key)] = model
            remaining_keys.remove(model.key)

        if not remaining_keys:
            cache.set_many(to_cache, 3600)
            return key_to_model
        try:
            with transaction.atomic():
                cls.objects.bulk_create([ cls(project_id=project_id, environment_id=environment_id, key=key) for key in remaining_keys
                                        ])
        except IntegrityError:
            pass
        else:
            for model in cls.objects.filter(project_id=project_id, environment_id=environment_id, key__in=remaining_keys):
                key_to_model[model.key] = to_cache[cls.get_cache_key(project_id, environment_id, model.key)] = model
                remaining_keys.remove(model.key)

            cache.set_many(to_cache, 3600)
            if not remaining_keys:
                return key_to_model

        for key in remaining_keys:
            key_to_model[key] = cls.get_or_create(project_id, environment_id, key)[0]

        return key_to_model