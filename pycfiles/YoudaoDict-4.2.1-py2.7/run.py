# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/youdao/service/run.py
# Compiled at: 2017-08-03 02:41:51
try:
    from twisted.internet import defer, reactor, protocol, endpoints
    from twisted.protocols.basic import LineReceiver
    from txmongo.connection import ConnectionPool
except ImportError:
    print 'This Service Require Following Dependencies:\n    twisted\n    txmongo\n\nand Databases:\n    mongodb\n    '
    exit(1)

import json, time
from youdao.spider import Spider
__author__ = 'hellflame'

class YoudaoProtocol(LineReceiver):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.connections += 1
        if self.factory.connections > self.factory.MAX_CONNECTIONS:
            self.transport.loseConnection()

    def connectionLost(self, reason=None):
        self.factory.connections -= 1

    def lineReceived(self, line):
        if len(line) > 100:
            self.transport.loseConnection()
        result = self.factory.get(line)

        def spider_consume(result):
            if result is not None:
                del result['_id']
                del result['key']
                self.transport.write(json.dumps(result) + '\r\n')
            self.transport.loseConnection()
            return

        def spider_error(err):
            self.transport.loseConnection()

        def done(result):
            if result:
                del result['_id']
                del result['key']
                self.transport.write(json.dumps(result) + '\r\n')
                self.transport.loseConnection()
            else:
                result = self.factory.spider_fetch(line)
                result.addCallback(spider_consume)
                result.addErrback(spider_error)

        def onError(err):
            self.transport.write('')
            self.transport.loseConnection()

        result.addErrback(onError)
        result.addCallback(done)


class YoudaoFactory(protocol.ServerFactory):

    def __init__(self, uri=None):
        if uri:
            mongodb = ConnectionPool(uri=uri)
        else:
            mongodb = ConnectionPool()
        self.db = mongodb.Youdao.Words
        self.connections = 0
        self.MAX_CONNECTIONS = 1024

    def buildProtocol(self, addr):
        return YoudaoProtocol(self)

    @defer.inlineCallbacks
    def get(self, target):
        result = yield self.db.find_one({'key': target})
        yield self.db.update({'key': target}, {'$inc': {'used': 1}})
        defer.returnValue(result)

    @defer.inlineCallbacks
    def spider_fetch(self, target):
        status, result = yield Spider().deploy(target)
        if result is not None:
            if not status:
                temp = result
                temp['key'] = target
                temp['insert_time'] = int(time.time())
                yield self.db.insert(temp)
        defer.returnValue(result)
        return


def main(port=3679):
    EndPoint = endpoints.serverFromString(reactor, ('tcp:{}').format(port))
    EndPoint.listen(YoudaoFactory())
    reactor.run()


if __name__ == '__main__':
    main(5001)