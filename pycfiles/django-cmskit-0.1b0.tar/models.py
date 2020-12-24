# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Ozgur/Sites/senpilic.com.tr/senpilic/utils/models.py
# Compiled at: 2012-10-05 05:05:42
from django.db import models

class Orderable(models.Model):
    """Add extra field and default ordering column for and inline orderable model"""
    ordering = models.IntegerField(blank=True, null=True, editable=True)

    class Meta:
        abstract = True
        ordering = ('ordering', )

    def save(self, force_insert=False, force_update=False, using=None):
        """Calculate position (max+1) for new records"""
        if not self.ordering:
            max = self.__class__.objects.filter().aggregate(models.Max('ordering'))
            try:
                self.ordering = max['ordering__max'] + 1
            except TypeError:
                self.ordering = 1

        return super(Orderable, self).save(force_insert=force_insert, force_update=force_update, using=using)