# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/nodes/models/status.py
# Compiled at: 2015-01-21 11:13:52
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseOrdered
from nodeshot.core.base.fields import RGBColorField

class Status(BaseOrdered):
    """
    Status of a node, eg: active, potential, approved
    """
    name = models.CharField(_('name'), max_length=255, help_text=_('label for this status, eg: active, approved, proposed'))
    slug = models.SlugField(max_length=75, db_index=True, unique=True)
    description = models.CharField(_('description'), max_length=255, help_text=_('this description will be used in the legend'))
    is_default = models.BooleanField(default=False, verbose_name=_('is default status?'), help_text=_('indicates whether this is the default status for new nodes;                    to change the default status to a new one just check and save,                    any other default will be automatically unchecked'))
    stroke_width = models.SmallIntegerField(blank=False, default=0, help_text=_('stroke of circles shown on map, set to 0 to disable'))
    fill_color = RGBColorField(_('fill colour'), blank=True)
    stroke_color = RGBColorField(_('stroke colour'), blank=True, default='#000000')
    text_color = RGBColorField(_('text colour'), blank=True, default='#FFFFFF')
    _current_is_default = False

    class Meta:
        db_table = 'nodes_status'
        app_label = 'nodes'
        verbose_name = _('status')
        verbose_name_plural = _('status')
        ordering = ['order']

    def __unicode__(self):
        return self.name

    def __init__(self, *args, **kwargs):
        """ Fill _current_is_default """
        super(Status, self).__init__(*args, **kwargs)
        if self.pk:
            self._current_is_default = self.is_default

    def save(self, *args, **kwargs):
        """ intercepts changes to is_default """
        ignore_default_check = kwargs.pop('ignore_default_check', False)
        if self.is_default != self._current_is_default and self.is_default is True:
            for status in self.__class__.objects.filter(is_default=True):
                status.is_default = False
                status.save(ignore_default_check=True)

        super(Status, self).save(*args, **kwargs)
        if self.__class__.objects.filter(is_default=True).count() == 0 and not ignore_default_check:
            self.is_default = True
            self.save()
        self._current_is_default = self.is_default