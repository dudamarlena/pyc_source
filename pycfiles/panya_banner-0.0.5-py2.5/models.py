# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/banner/models.py
# Compiled at: 2010-12-14 06:48:44
from django.db import models
from panya.models import ModelBase
from preferences.models import Preferences

class Banner(ModelBase):
    pass


class CodeBanner(Banner):
    code = models.TextField(help_text='The full HTML/Javascript code snippet to be embedded for this banner.')

    class Meta:
        verbose_name = 'Code banner'
        verbose_name_plural = 'Code banners'


class ImageBanner(Banner):
    url = models.CharField(max_length='256', verbose_name='URL', help_text='URL (internal or external) to which this banner will link.')

    class Meta:
        verbose_name = 'Image banner'
        verbose_name_plural = 'Image banners'

    def get_absolute_url(self):
        return self.url


class BannerPreferences(Preferences):
    __module__ = 'preferences.models'

    class Meta:
        verbose_name = 'Banner preferences'
        verbose_name_plural = 'Banner preferences'


class BannerOption(models.Model):
    banner_preferences = models.ForeignKey('preferences.BannerPreferences')
    is_default = models.BooleanField(verbose_name='Default', default=False)
    url_name = models.CharField(max_length=256, verbose_name='URL Name', blank=True, null=True)
    url = models.CharField(max_length=256, verbose_name='URL (takes precedence)', blank=True, null=True)
    banner = models.ForeignKey('banner.Banner')
    position = models.CharField(max_length=256)