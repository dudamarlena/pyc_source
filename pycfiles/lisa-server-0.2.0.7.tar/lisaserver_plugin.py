# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Sandbox/LISA/twisted/plugins/lisaserver_plugin.py
# Compiled at: 2014-08-02 03:34:25
from zope.interface import implements
from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from lisa.server import service

class Options(usage.Options):
    optParameters = [
     [
      'configuration', 'c', '/etc/lisa/server/configuration/lisa.json']]


class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'lisa-server'
    description = 'Lisa server.'
    options = Options

    def makeService(self, config):
        return service.makeService(config)


serviceMaker = ServiceMaker()