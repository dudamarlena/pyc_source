# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/ondelta/models.py
# Compiled at: 2016-07-11 15:54:41
import copy, logging
from django.db import models
from django.utils.functional import cached_property
from .signals import post_ondelta_signal
logger = logging.getLogger('ondelta')

class OnDeltaMixin(models.Model):

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(OnDeltaMixin, self).__init__(*args, **kwargs)
        if self.pk:
            self._ondelta_take_snapshot()
        else:
            self._ondelta_shadow = None
        return

    @cached_property
    def _ondelta_fields_to_watch(self):
        """
        This gives us all the fields that we should care about changes
        for, excludes fields added by tests (nose adds 'c') and the id
        which is an implementation detail of django.

        Child classes may override this method to limit the set of
        fields watched by ondelta.
        """
        return [ f.name for f in self._meta.fields if f.name not in {'c', 'id'} ]

    def _ondelta_take_snapshot(self):
        self._ondelta_shadow = copy.copy(self)

    def _ondelta_get_differences(self):
        assert self._ondelta_shadow is not None
        fields_changed = dict()
        for field_name in self._ondelta_fields_to_watch:
            try:
                snapshot_value = getattr(self._ondelta_shadow, field_name)
            except:
                logger.exception(('Failed to retrieve the old value of {model}.{field} for comparison').format(model=self.__class__.__name__, field=field_name))
                continue

            try:
                current_value = getattr(self, field_name)
            except:
                logger.exception(('Failed to retrieve the new value of {model}.{field} for comparison').format(model=self.__class__.__name__, field=field_name))
                continue

            if snapshot_value != current_value:
                fields_changed[field_name] = {'old': snapshot_value, 'new': current_value}

        return fields_changed

    def _ondelta_dispatch_notifications(self, fields_changed, recursing=False):
        self._ondelta_take_snapshot()
        for field, changes in fields_changed.items():
            method = getattr(self, ('ondelta_{field}').format(field=field), None)
            if method is not None:
                method(changes['old'], changes['new'])

        self.ondelta_all(fields_changed=fields_changed)
        fields_changed_by_ondelta_methods = self._ondelta_get_differences()
        if fields_changed_by_ondelta_methods:
            self._ondelta_dispatch_notifications(fields_changed_by_ondelta_methods, recursing=True)
            if not recursing:
                self.save()
        return

    def ondelta_all(self, fields_changed):
        """
        Child classes interested in executing logic based upon
        aggregate field changes should override this method
        """
        pass

    def save(self, *args, **kwargs):
        super_return = super(OnDeltaMixin, self).save(*args, **kwargs)
        if self._ondelta_shadow is None:
            self._ondelta_take_snapshot()
        else:
            fields_changed = self._ondelta_get_differences()
            if fields_changed:
                self._ondelta_dispatch_notifications(fields_changed)
                post_ondelta_signal.send(sender=self.__class__, fields_changed=fields_changed, instance=self)
        return super_return