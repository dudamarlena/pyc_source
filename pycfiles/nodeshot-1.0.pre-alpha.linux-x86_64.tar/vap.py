# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/net/models/interfaces/vap.py
# Compiled at: 2013-09-08 06:03:46
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate
from nodeshot.networking.net.models import Interface

class Vap(BaseDate):
    """
    VAP interface
    represents a virtual wireless interface
    """
    interface = models.ForeignKey('net.Wireless', verbose_name='wireless interface')
    essid = models.CharField(max_length=50, null=True, blank=True)
    bssid = models.CharField(max_length=50, null=True, blank=True)
    encryption = models.CharField(max_length=50, null=True, blank=True)
    key = models.CharField(max_length=100, null=True, blank=True)
    auth_server = models.CharField(max_length=50, null=True, blank=True)
    auth_port = models.IntegerField(null=True, blank=True)
    accounting_server = models.CharField(max_length=50, null=True, blank=True)
    accounting_port = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.essid

    class Meta:
        app_label = 'net'
        db_table = 'net_interface_vap'
        verbose_name = _('vap interface')
        verbose_name_plural = _('vap interfaces')