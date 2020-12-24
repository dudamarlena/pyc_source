# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mimir/monitor/tap.py
# Compiled at: 2012-05-10 08:39:36
"""
Create a monitor service.
"""
from twisted.application import service
from twisted.enterprise import adbapi
from twisted.python import usage
from twisted.words.protocols.jabber import jid
from wokkel import client
from wokkel.iwokkel import IXMPPHandler
from mimir.monitor import news, presence

class Options(usage.Options):
    optParameters = [
     ('jid', None, None),
     ('secret', None, None),
     ('dbuser', None, None),
     ('dbname', None, 'mimir')]
    optFlags = [
     ('verbose', 'v', 'Show traffic')]

    def postOptions(self):
        try:
            self['jid'] = jid.JID(self['jid'])
        except jid.InvalidFormat:
            raise usage.UsageError("'%(jid)s' is not a valid Jabber ID" % self)

        if not self['secret']:
            raise usage.UsageError('No secret provided')


def makeService(config):
    s = service.MultiService()
    clientService = client.XMPPClient(config['jid'], config['secret'])
    clientService.setServiceParent(s)
    clientService.factory.maxDelay = 900
    if config['verbose']:
        clientService.logTraffic = True
    dbpool = adbapi.ConnectionPool('pyPgSQL.PgSQL', user=config['dbuser'], database=config['dbname'], client_encoding='utf-8', cp_min=1, cp_max=1, cp_reconnect=True)
    ms = presence.Storage(dbpool)
    presenceMonitor = presence.RosterMonitor(ms)
    presenceMonitor.setHandlerParent(clientService)
    newsService = news.NewsService(presenceMonitor, dbpool)
    newsService.setServiceParent(s)
    xep = IXMPPHandler(newsService)
    newsService.notifier = xep
    xep.setHandlerParent(clientService)
    return s