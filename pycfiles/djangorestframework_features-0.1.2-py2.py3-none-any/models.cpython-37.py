# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dev/dev/django-rest-framework-features/rest_framework_features/models.py
# Compiled at: 2019-10-04 11:16:55
# Size of source mod 2**32: 1281 bytes
from django.db import models
import django.utils.translation as _

class AbstractBaseFeature(models.Model):

    class Meta:
        abstract = True
        unique_together = ('parent', 'name')
        ordering = ('hierarchical_name', )

    created_timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(verbose_name=(_('name')),
      max_length=64)
    parent = models.ForeignKey(verbose_name=(_('parent')),
      to='self',
      blank=True,
      null=True,
      on_delete=(models.CASCADE),
      related_name='children')
    hierarchical_name = models.CharField(verbose_name=(_('name')),
      max_length=256)

    def save(self, *args, **kwargs):
        if not self.hierarchical_name:
            if self.parent_id:
                self.hierarchical_name = '/'.join([self.parent.hierarchical_name, self.name])
            else:
                self.hierarchical_name = self.name
        return (super().save)(*args, **kwargs)

    def __str__(self):
        return self.hierarchical_name


class Feature(AbstractBaseFeature):

    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')


__all__ = ('AbstractBaseFeature', 'Feature')