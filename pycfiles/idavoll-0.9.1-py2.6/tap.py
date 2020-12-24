# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idavoll/tap.py
# Compiled at: 2009-09-07 02:55:31
from twisted.application import service
from twisted.python import usage
from twisted.words.protocols.jabber.jid import JID
from wokkel.component import Component
from wokkel.disco import DiscoHandler
from wokkel.generic import FallbackHandler, VersionHandler
from wokkel.iwokkel import IPubSubService
from idavoll import __version__
from idavoll.backend import BackendService

class Options(usage.Options):
    optParameters = [
     ('jid', None, 'pubsub', 'JID this component will be available at'),
     ('secret', None, 'secret', 'Jabber server component secret'),
     ('rhost', None, '127.0.0.1', 'Jabber server host'),
     ('rport', None, '5347', 'Jabber server port'),
     ('backend', None, 'memory', 'Choice of storage backend'),
     ('dbuser', None, None, 'Database user (pgsql backend)'),
     ('dbname', None, 'pubsub', 'Database name (pgsql backend)'),
     ('dbpass', None, None, 'Database password (pgsql backend)'),
     ('dbhost', None, None, 'Database host (pgsql backend)'),
     ('dbport', None, None, 'Database port (pgsql backend)')]
    optFlags = [
     ('verbose', 'v', 'Show traffic'),
     ('hide-nodes', None, 'Hide all nodes for disco')]

    def postOptions(self):
        if self['backend'] not in ('pgsql', 'memory'):
            raise usage.UsageError, 'Unknown backend!'
        self['jid'] = JID(self['jid'])


def makeService(config):
    s = service.MultiService()
    if config['backend'] == 'pgsql':
        from twisted.enterprise import adbapi
        from idavoll.pgsql_storage import Storage
        dbpool = adbapi.ConnectionPool('pyPgSQL.PgSQL', user=config['dbuser'], password=config['dbuser'], database=config['dbname'], host=config['dbpass'], port=config['dbport'], cp_reconnect=True, client_encoding='utf-8')
        st = Storage(dbpool)
    elif config['backend'] == 'memory':
        from idavoll.memory_storage import Storage
        st = Storage()
    bs = BackendService(st)
    bs.setName('backend')
    bs.setServiceParent(s)
    cs = Component(config['rhost'], int(config['rport']), config['jid'].full(), config['secret'])
    cs.setName('component')
    cs.setServiceParent(s)
    cs.factory.maxDelay = 900
    if config['verbose']:
        cs.logTraffic = True
    FallbackHandler().setHandlerParent(cs)
    VersionHandler('Idavoll', __version__).setHandlerParent(cs)
    DiscoHandler().setHandlerParent(cs)
    ps = IPubSubService(bs)
    ps.setHandlerParent(cs)
    ps.hideNodes = config['hide-nodes']
    ps.serviceJID = config['jid']
    return s