# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/models/tracked.py
# Compiled at: 2018-11-06 06:10:45
# Size of source mod 2**32: 2013 bytes
from django.conf import settings
from django.db import models
from django.utils import timezone
__all__ = [
 'DateTracked', 'StatusTracked', 'PositionTracked', 'FullTracked']

class DateTracked(models.Model):
    created_at = models.DateTimeField('Créé le', auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField('Modifié le', auto_now=True, db_index=True, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.updated_at:
            self.updated_at = timezone.now()
        (super().save)(*args, **kwargs)


class StatusTracked(models.Model):
    is_active = models.BooleanField('Activé', default=True)
    is_deleted = models.BooleanField('Supprimé', default=False)

    class Meta:
        abstract = True


class PositionTracked(models.Model):
    position = models.PositiveIntegerField('Position', default=0)

    class Meta:
        abstract = True


class FullTracked(DateTracked, StatusTracked, PositionTracked):
    created_by = models.ForeignKey((settings.AUTH_USER_MODEL), verbose_name='Créé par', related_name='+', null=True, blank=True, on_delete=(models.SET_NULL))
    created_by_repr = models.CharField('Créé par', max_length=254, null=True, blank=True)
    updated_by = models.ForeignKey((settings.AUTH_USER_MODEL), verbose_name='Modifié par', related_name='+', null=True, blank=True, on_delete=(models.SET_NULL))
    updated_by_repr = models.CharField('Modifié par', max_length=254, null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        edited_by = kwargs.pop('edited_by', None)
        if edited_by:
            if not self.created_by_id:
                self.created_by = edited_by
                self.created_by_repr = str(edited_by)
            self.updated_by = edited_by
            self.updated_by_repr = str(edited_by)
        (super().save)(**kwargs)