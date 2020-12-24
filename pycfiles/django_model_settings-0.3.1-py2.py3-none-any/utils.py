# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: model_settings/utils.py
# Compiled at: 2018-01-16 16:05:11
import django
from django.db import transaction

def get_all_related_objects(opts):
    if django.VERSION < (1, 8):
        return opts.get_all_related_objects()
    else:
        return [ r for r in opts.related_objects if not r.field.many_to_many ]


class SettingDict(dict):
    """
    Provides a read/write dict-like interface for ``Setting`` objects.

    Caches setting values for efficiency. Call the ``refresh()`` method to
    re-fetch all values from the database, if the cache becomes stale.
    """

    def __init__(self, model=None, queryset=None, default=None):
        """
        All setting values for the given model or queryset will be lazily
        loaded into the cache on first access.

        If ``default`` is not ``None``, non-existent settings will be created
        on access.
        """
        if model:
            self.model = model
            self.queryset = model.objects.all()
        elif queryset is not None:
            if model:
                raise ValueError('Only one of `model` or `queryset` can be provided.')
            self.model = queryset.model
            self.queryset = queryset
        else:
            raise ValueError('At least one of `model` or `queryset` must be provided.')
        self.default = default
        self.empty_cache = True
        super(SettingDict, self).__init__()
        return

    def __delitem__(self, key):
        """
        Deletes a setting from the dict and the database.
        """
        if self.empty_cache:
            self.refresh()
        deleted = self.model.objects.filter(name=key).delete()
        try:
            super(SettingDict, self).__delitem__(key)
        except KeyError:
            if not deleted:
                raise

    def __getitem__(self, key):
        """
        Returns the setting value for ``key`` from the cache if possible,
        otherwise from the database. Adds values that are fetched from the
        database to the cache.
        """
        if self.empty_cache:
            self.refresh()
        try:
            value = super(SettingDict, self).__getitem__(key)
        except KeyError:
            try:
                value = self.model.objects.get(name=key).value
            except self.model.DoesNotExist:
                if self.default is None:
                    raise KeyError(key)
                value = self.default
                self.model.objects.create(name=key, value=value)

            super(SettingDict, self).__setitem__(key, value)

        return value

    def __setitem__(self, key, value):
        """
        Tries to delete and then creates a setting, in case the value type has
        changed. Otherwise, we would need to get, update (if same type), or
        delete and create (if not same type).
        """
        if self.empty_cache:
            self.refresh()
        with transaction.atomic():
            self.model.objects.filter(name=key).delete()
            self.model.objects.create(name=key, value=value)
        super(SettingDict, self).__setitem__(key, value)

    def refresh(self):
        """
        Updates the cache with setting values from the database.
        """
        args = [ (obj.name, obj.value) for obj in self.queryset.all() ]
        super(SettingDict, self).update(args)
        self.empty_cache = False