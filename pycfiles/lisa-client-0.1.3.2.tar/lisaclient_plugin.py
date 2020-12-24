# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seraf/Sandbox/LISA-CLIENT-Linux/twisted/plugins/lisaclient_plugin.py
# Compiled at: 2014-09-02 17:11:00
from zope.interface import implements
from twisted.python import usage
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from lisa.client import service

class Options(usage.Options):
    optParameters = [
     [
      'configuration', 'c', '/etc/lisa/client/configuration/lisa.json']]


class ServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'lisa-client'
    description = 'Lisa client.'
    options = Options

    def makeService(self, config):
        return service.makeService(config)


serviceMaker = ServiceMaker()