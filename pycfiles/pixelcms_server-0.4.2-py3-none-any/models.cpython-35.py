# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mw/dev/pixelcms-server/cms/settings/models.py
# Compiled at: 2016-12-31 04:02:59
# Size of source mod 2**32: 1017 bytes
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.common.fields import LanguageField

class Settings(models.Model):
    language = LanguageField(_('language'), unique=True)
    site_name = models.CharField(_('site name'), max_length=255, blank=True, default='PixelCMS site')
    page_title_site_name_suffix = models.BooleanField(_('site name suffix in page title'), default=True)
    suffix_separator = models.CharField(_('suffix separator'), max_length=10, default='|')
    meta_description = models.CharField(_('description'), max_length=255, blank=True, default='')
    meta_robots = models.CharField(_('robots'), max_length=255, blank=True, default='index, follow')

    class Meta:
        app_label = 'settings'
        ordering = ('language', )
        verbose_name = _('general settings')
        verbose_name_plural = _('general settings')

    def __str__(self):
        return self.language