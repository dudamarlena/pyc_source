# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/filip/src/projects/macht/mezzanine_references/models.py
# Compiled at: 2015-05-26 11:39:11
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.models import Orderable
from mezzanine.pages.models import Page

class References(Page):
    image_style = models.CharField(_('Image style'), choices=(
     (
      'rounded', _('Rounded')),
     (
      'circle', _('Circle')),
     (
      'thumbnail', _('Thumbnail')),
     (
      'default', _('Default'))), default='default', max_length=12)
    image_size = models.PositiveIntegerField(_('Image width in pixels'), default=200)
    link_style = models.CharField(_('Link style'), choices=(
     (
      'button', _('Button')),
     (
      'text', _('Text'))), default='button', max_length=12)
    button_style = models.CharField(_('Button style'), choices=(
     ('default', 'default'),
     ('primary', 'primary'),
     ('info', 'info'),
     ('warning', 'warning'),
     ('danger', 'danger')), default='default', max_length=12)


class Reference(Orderable):
    page = models.ForeignKey(References)
    content = models.TextField(_('Content'))
    name = models.CharField(_('Name'), max_length=32)
    date = models.DateField(_('Date of realization'), null=True, blank=True)
    image = models.ImageField(upload_to='references', null=True, blank=True)
    link = models.CharField(_('Link'), max_length=128, null=True, blank=True)
    link_title = models.CharField(_('Link title'), max_length=32, null=True, blank=True)
    link_new_window = models.BooleanField(_('Open link on new page'), default=False)

    class Meta:
        order_with_respect_to = 'page'