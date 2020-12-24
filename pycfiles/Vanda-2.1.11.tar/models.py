# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/page/models.py
# Compiled at: 2013-01-07 03:52:15
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.contrib.sites.models import Site
from django.conf import settings

class Page(models.Model):
    """
    Page main model class
    """
    user = models.ForeignKey(User, editable=False, verbose_name=_('User'))
    title = models.CharField(max_length=30, verbose_name=_('Title'))
    slug = models.SlugField(max_length=30, unique=True, verbose_name=_('Slug'))
    content = models.TextField(verbose_name=_('Page content'))
    site = models.ForeignKey(Site, verbose_name=_('Site'))
    language = models.CharField(_('Language'), max_length=4, choices=settings.LANGUAGES, default=settings.LANGUAGES[0][0])
    publish = models.BooleanField(default=False, verbose_name=_('Publish'))
    menu = models.BooleanField(default=False, verbose_name=_('Appear in navigation?'))
    weight = models.IntegerField(default=40, verbose_name=_('Weight'))
    date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name=_('Date and Time'))

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return 'page.views.show_page' % self.slug

    class Meta:
        verbose_name_plural = _('Pages')
        verbose_name = _('Page')
        ordering = ['-weight']