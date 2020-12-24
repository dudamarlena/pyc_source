# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idavoll/tap_http.py
# Compiled at: 2009-07-15 05:50:51
from twisted.application import internet, service, strports
from twisted.conch import manhole, manhole_ssh
from twisted.cred import portal, checkers
from twisted.web2 import channel, log, resource, server
from twisted.web2.tap import Web2Service
from idavoll import gateway, tap
from idavoll.gateway import RemoteSubscriptionService

class Options(tap.Options):
    optParameters = [
     ('webport', None, '8086', 'Web port')]


def getManholeFactory(namespace, **passwords):

    def getManHole(_):
        return manhole.Manhole(namespace)

    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = getManHole
    p = portal.Portal(realm)
    p.registerChecker(checkers.InMemoryUsernamePasswordDatabaseDontUse(**passwords))
    f = manhole_ssh.ConchFactory(p)
    return f


def makeService(config):
    s = tap.makeService(config)
    bs = s.getServiceNamed('backend')
    cs = s.getServiceNamed('component')
    if config['backend'] == 'pgsql':
        from idavoll.pgsql_storage import GatewayStorage
        gst = GatewayStorage(bs.storage.dbpool)
    elif config['backend'] == 'memory':
        from idavoll.memory_storage import GatewayStorage
        gst = GatewayStorage()
    ss = RemoteSubscriptionService(config['jid'], gst)
    ss.setHandlerParent(cs)
    ss.startService()
    root = resource.Resource()
    root.child_create = gateway.CreateResource(bs, config['jid'], config['jid'])
    root.child_delete = gateway.DeleteResource(bs, config['jid'], config['jid'])
    root.child_publish = gateway.PublishResource(bs, config['jid'], config['jid'])
    root.child_list = gateway.ListResource(bs)
    root.child_subscribe = gateway.RemoteSubscribeResource(ss)
    root.child_unsubscribe = gateway.RemoteUnsubscribeResource(ss)
    root.child_items = gateway.RemoteItemsResource(ss)
    if config['verbose']:
        root = log.LogWrapperResource(root)
    site = server.Site(root)
    w = internet.TCPServer(int(config['webport']), channel.HTTPFactory(site))
    if config['verbose']:
        logObserver = log.DefaultCommonAccessLoggingObserver()
        w2s = Web2Service(logObserver)
        w.setServiceParent(w2s)
        w = w2s
    w.setServiceParent(s)
    namespace = {'service': s, 'component': cs, 
       'backend': bs, 
       'root': root}
    f = getManholeFactory(namespace, admin='admin')
    manholeService = strports.service('2222', f)
    manholeService.setServiceParent(s)
    return s