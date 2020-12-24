# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/models.py
# Compiled at: 2014-06-19 02:59:31
# Size of source mod 2**32: 3496 bytes
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.db import models
from ghostdown.models.fields import GhostdownField

@python_2_unicode_compatible
class Application(models.Model):
    __doc__ = 'Representation of a Cocoa application.'
    name = models.CharField(max_length=50, verbose_name=_('name'))
    slug = models.SlugField(max_length=50, unique=True, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('application')
        verbose_name_plural = _('applications')

    def __str__(self):
        return self.name

    def active_versions(self):
        return self.versions.filter(publish_at__lte=now())


@python_2_unicode_compatible
class Version(models.Model):
    __doc__ = 'A version for a given application.'
    application = models.ForeignKey('Application', related_name='versions', verbose_name=_('application'))
    title = models.CharField(max_length=100, verbose_name=_('title'))
    version = models.CharField(max_length=10, verbose_name=_('version'), help_text='If you use short_version, this can be the internal version number or build number that will not be shown. In any case, this string is compared to CFBundleVersion of your bundle.')
    short_version = models.CharField(max_length=50, blank=True, verbose_name=_('short version'), help_text='A user-displayable version string.')
    dsa_signature = models.CharField(max_length=80, verbose_name=_('DSA signature'))
    length = models.CharField(max_length=20, verbose_name=_('length'))
    release_notes = GhostdownField(blank=True, verbose_name=_('release notes'))
    minimum_system_version = models.CharField(max_length=10, verbose_name=_('minimum system version'))
    update_url = models.URLField(max_length=200, verbose_name=_('update URL'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    publish_at = models.DateTimeField(default=now, verbose_name=_('published at'), help_text='When this upate will be (automatically) published.')

    class Meta:
        verbose_name = _('version')
        verbose_name_plural = _('versions')
        ordering = ('-publish_at', )

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class SystemProfileReport(models.Model):
    __doc__ = 'A system profile report.'
    ip_address = models.IPAddressField(verbose_name=_('IP address'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    def __str__(self):
        return _('From {ip} at {t}').format(ip=self.ip_address, t=self.created_at)


@python_2_unicode_compatible
class SystemProfileReportRecord(models.Model):
    __doc__ = 'A key-value pair for a system profile report.'
    report = models.ForeignKey('SystemProfileReport', verbose_name=_('report'))
    key = models.CharField(max_length=100, verbose_name=_('key'))
    value = models.CharField(max_length=80, verbose_name=_('value'))

    def __str__(self):
        return '{key}:{value}'.format(key=self.key, value=self.value)