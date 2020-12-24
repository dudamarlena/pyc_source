# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/hardware/models/mac_prefix.py
# Compiled at: 2014-05-08 09:17:59
from django.db import models
from django.utils.translation import ugettext_lazy as _
from . import Manufacturer

class MacPrefix(models.Model):
    """ Mac prefix of a Manufacturer """
    manufacturer = models.ForeignKey(Manufacturer, verbose_name=_('manufacturer'))
    prefix = models.CharField(_('mac address prefix'), max_length=8, unique=True)

    def __unicode__(self):
        return self.prefix

    class Meta:
        app_label = 'hardware'
        verbose_name = _('MAC Prefix')
        verbose_name_plural = _('MAC Prefixes')