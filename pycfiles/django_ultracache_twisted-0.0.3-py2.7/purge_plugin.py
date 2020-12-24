# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/django-ultracache-twisted/twisted/plugins/purge_plugin.py
# Compiled at: 2017-06-06 14:48:03
from zope.interface import implements
from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
import purge

class Options(usage.Options):
    optParameters = [
     [
      'config', 'c', '', 'Optional config file']]


class PurgeServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'purge'
    description = 'Subscribe to RabbitMQ fanout exchange called purgatory and send purge instruction to a reverse caching proxy.'
    options = Options

    def makeService(self, options):
        return purge.makeService(options)


serviceMaker = PurgeServiceMaker()