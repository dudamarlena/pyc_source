# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/twisted/plugins/spamfighter_plugin.py
# Compiled at: 2009-01-30 08:10:10
"""
Плагин для запуска СпамоБорца через twistd.
"""
from zope.interface import implements
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker
from twisted.python import usage
from spamfighter import service

class SpamFighterServiceMaker(object):
    implements(IServiceMaker, IPlugin)
    tapname = 'spamfighter'
    description = 'A Spam Fighter web service'
    options = usage.Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        return service.makeService()


serviceMaker = SpamFighterServiceMaker()