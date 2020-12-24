# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/net/models/interfaces/ethernet.py
# Compiled at: 2013-09-08 06:03:46
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.networking.net.models import Interface
from nodeshot.networking.net.models.choices import ETHERNET_STANDARDS, DUPLEX_CHOICES, INTERFACE_TYPES

class Ethernet(Interface):
    """ Ethernet Interface """
    standard = models.CharField(_('standard'), max_length=15, choices=ETHERNET_STANDARDS)
    duplex = models.CharField(_('duplex?'), max_length=15, choices=DUPLEX_CHOICES)
    objects = Interface.objects.__class__()

    class Meta:
        app_label = 'net'
        db_table = 'net_interface_ethernet'
        verbose_name = _('ethernet interface')
        verbose_name_plural = _('ethernet interfaces')

    def save(self, *args, **kwargs):
        """ automatically set Interface.type to ethernet """
        self.type = INTERFACE_TYPES.get('ethernet')
        super(Ethernet, self).save(*args, **kwargs)