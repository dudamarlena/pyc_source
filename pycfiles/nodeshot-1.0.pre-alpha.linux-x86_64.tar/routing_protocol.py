# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/net/models/routing_protocol.py
# Compiled at: 2013-12-29 12:41:48
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.base.models import BaseDate
from choices import ROUTING_PROTOCOLS

class RoutingProtocol(BaseDate):
    """ Routing Protocol Model """
    name = models.CharField(_('name'), max_length=50, choices=ROUTING_PROTOCOLS)
    version = models.CharField(_('version'), max_length=128, blank=True)

    class Meta:
        app_label = 'net'
        db_table = 'net_routing_protocol'
        unique_together = ('name', 'version')

    def __unicode__(self):
        return '%s %s' % (self.name, self.version)