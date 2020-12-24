# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/PROGETTI/saxix/django-project-settings/project_settings/models.py
# Compiled at: 2014-09-14 10:16:33
from __future__ import unicode_literals
from django.conf import settings as django_settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Setting(models.Model):
    """
    Stores values for ``mezzanine.conf`` that can be edited via the admin.
    """
    prefix = models.CharField(max_length=50)
    name = models.CharField(max_length=150, unique=True)
    value = models.CharField(max_length=2000)
    site = models.ForeignKey(b'sites.Site', editable=False, related_name=b'project_setting', default=django_settings.SITE_ID)

    class Meta:
        verbose_name = _(b'Setting')
        verbose_name_plural = _(b'Settings')

    def __str__(self):
        return b'%s: %s' % (self.name, self.value)

    def save(self, update_site=False, *args, **kwargs):
        """
        Set the site to the current site when the record is first
        created, or the ``update_site`` argument is explicitly set
        to ``True``.
        """
        if update_site or not self.id:
            self.site_id = django_settings.SITE_ID
        super(Setting, self).save(*args, **kwargs)
        from .conf import settings
        settings._loaded = False
        settings._editable_cache[self.name] = self.value