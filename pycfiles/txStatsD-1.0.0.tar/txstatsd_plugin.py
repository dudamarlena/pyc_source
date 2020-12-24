# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sidnei/src/txstatsd/trunk/twisted/plugins/txstatsd_plugin.py
# Compiled at: 2012-06-28 13:21:31
from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from txstatsd import service

class StatsDServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'statsd'
    description = 'Collect and aggregate stats for graphite.'
    options = service.StatsDOptions

    def makeService(self, options):
        """
        Construct a StatsD service.
        """
        return service.createService(options)


serviceMaker = StatsDServiceMaker()