# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/modelversions/models.py
# Compiled at: 2015-09-15 09:39:08
from django.db import models
from django.db.models import F, signals
from django.db import router, transaction
from django.db.models.fields import AutoField
from django.db import DatabaseError

class ConcurrentModificationException(Exception):
    pass


class VersionedModel(models.Model):
    _version = models.IntegerField(null=False, blank=True)

    def save_base_with_version(self, raw=False, force_insert=False, force_update=False, using=None, update_fields=None):
        using = using or router.db_for_write(self.__class__, instance=self)
        if not not (force_insert and (force_update or update_fields)):
            raise AssertionError
            if not (update_fields is None or len(update_fields) > 0):
                raise AssertionError
                cls = origin = self.__class__
                if cls._meta.proxy:
                    cls = cls._meta.concrete_model
                meta = cls._meta
                if not meta.auto_created:
                    signals.pre_save.send(sender=origin, instance=self, raw=raw, using=using, update_fields=update_fields)
                non_pks = [ f for f in meta.local_fields if not f.primary_key ]
                if update_fields:
                    non_pks = [ f for f in non_pks if f.name in update_fields or f.attname in update_fields ]
                pk_val = self._get_pk_val(meta)
                record_exists = True
                manager = cls._base_manager
                values = []
                for f in non_pks:
                    if f.name == '_version':
                        values.append((f, None, F('_version') + 1))
                    else:
                        values.append((f, None, raw and getattr(self, f.attname) or f.pre_save(self, False)))

                if values:
                    with transaction.atomic(savepoint=False):
                        rows = manager.using(using).filter(pk=pk_val, _version=self._version)._update(values)
                    raise (rows or ConcurrentModificationException)('Model updated already, was version %d' % self._version)
                self._version += 1
                if force_update and not rows:
                    raise DatabaseError('Forced update did not affect any rows.')
                if update_fields and not rows:
                    raise DatabaseError('Save with update_fields did not affect any rows.')
            self._state.db = using
            self._state.adding = False
            meta.auto_created or signals.post_save.send(sender=origin, instance=self, created=not record_exists, update_fields=update_fields, raw=raw, using=using)
        return

    def save_base(self, raw=False, force_insert=False, force_update=False, using=None, update_fields=None):
        """If this model already exists then this performs an update to ensure
        that the model has not already been updated."""
        if self._version:
            return self.save_base_with_version(raw, force_insert, force_update, using, update_fields)
        else:
            self._version = 1
            return super(VersionedModel, self).save_base(raw=raw, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    save_base.alters_data = True

    class Meta:
        abstract = True