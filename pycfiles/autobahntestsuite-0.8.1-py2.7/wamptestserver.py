# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/wamptestserver.py
# Compiled at: 2018-12-17 11:51:20
import math, shelve, decimal
from twisted.internet import reactor, defer
from autobahn.wamp1.protocol import exportRpc, exportSub, exportPub, WampServerFactory, WampServerProtocol

class Simple:
    """
   A simple calc service we will export for Remote Procedure Calls (RPC).

   All you need to do is use the @exportRpc decorator on methods
   you want to provide for RPC and register a class instance in the
   server factory (see below).

   The method will be exported under the Python method name, or
   under the (optional) name you can provide as an argument to the
   decorator (see asyncSum()).
   """

    @exportRpc
    def add(self, x, y):
        return x + y

    @exportRpc
    def sub(self, x, y):
        return x - y

    @exportRpc
    def square(self, x):
        if x > 1000:
            raise Exception('http://example.com/error#number_too_big', 'number %d too big to square' % x)
        return x * x

    @exportRpc
    def sum(self, list):
        return reduce(lambda x, y: x + y, list)

    @exportRpc
    def pickySum(self, list):
        errs = []
        for i in list:
            if i % 3 == 0:
                errs.append(i)

        if len(errs) > 0:
            raise Exception('http://example.com/error#invalid_numbers', 'one or more numbers are multiples of 3', errs)
        return reduce(lambda x, y: x + y, list)

    @exportRpc
    def sqrt(self, x):
        return math.sqrt(x)

    @exportRpc('asum')
    def asyncSum(self, list):
        d = defer.Deferred()
        reactor.callLater(3, d.callback, self.sum(list))
        return d


class KeyValue:
    """
   Simple, persistent key-value store.
   """

    def __init__(self, filename):
        self.store = shelve.open(filename)

    @exportRpc
    def set(self, key=None, value=None):
        if key is not None:
            k = str(key)
            if value is not None:
                self.store[k] = value
            elif self.store.has_key(k):
                del self.store[k]
        else:
            self.store.clear()
        return

    @exportRpc
    def get(self, key=None):
        if key is None:
            return self.store.items()
        else:
            return self.store.get(str(key), None)
            return

    @exportRpc
    def keys(self):
        return self.store.keys()


class Calculator:
    """
   Woooohoo. Simple decimal arithmetic calculator.
   """

    def __init__(self):
        self.clear()

    def clear(self, arg=None):
        self.op = None
        self.current = decimal.Decimal(0)
        return

    @exportRpc
    def calc(self, arg):
        op = arg['op']
        if op == 'C':
            self.clear()
            return str(self.current)
        num = decimal.Decimal(arg['num'])
        if self.op:
            if self.op == '+':
                self.current += num
            elif self.op == '-':
                self.current -= num
            elif self.op == '*':
                self.current *= num
            elif self.op == '/':
                self.current /= num
            self.op = op
        else:
            self.op = op
            self.current = num
        res = str(self.current)
        if op == '=':
            self.clear()
        return res


class MyTopicService:

    def __init__(self, allowedTopicIds):
        self.allowedTopicIds = allowedTopicIds
        self.serial = 0

    @exportSub('foobar', True)
    def subscribe(self, topicUriPrefix, topicUriSuffix):
        """
      Custom topic subscription handler.
      """
        print 'client wants to subscribe to %s%s' % (topicUriPrefix, topicUriSuffix)
        try:
            i = int(topicUriSuffix)
            if i in self.allowedTopicIds:
                print 'Subscribing client to topic Foobar %d' % i
                return True
            print 'Client not allowed to subscribe to topic Foobar %d' % i
            return False
        except:
            print 'illegal topic - skipped subscription'
            return False

    @exportPub('foobar', True)
    def publish(self, topicUriPrefix, topicUriSuffix, event):
        """
      Custom topic publication handler.
      """
        print 'client wants to publish to %s%s' % (topicUriPrefix, topicUriSuffix)
        try:
            i = int(topicUriSuffix)
            if type(event) == dict and event.has_key('count'):
                if event['count'] > 0:
                    self.serial += 1
                    event['serial'] = self.serial
                    print 'ok, published enriched event'
                    return event
                else:
                    print 'event count attribute is negative'
                    return

            else:
                print 'event is not dict or misses count attribute'
                return
        except:
            print 'illegal topic - skipped publication of event'
            return

        return


class WampTestServerProtocol(WampServerProtocol):

    def onSessionOpen(self):
        self.initSimpleRpc()
        self.initKeyValue()
        self.initCalculator()
        self.initSimplePubSub()
        self.initPubSubAuth()

    def initSimpleRpc(self):
        self.simple = Simple()
        self.registerForRpc(self.simple, 'http://example.com/simple/calc#')

    def initKeyValue(self):
        self.registerForRpc(self.factory.keyvalue, 'http://example.com/simple/keyvalue#')

    def initCalculator(self):
        self.calculator = Calculator()
        self.registerForRpc(self.calculator, 'http://example.com/simple/calculator#')

    def initSimplePubSub(self):
        self.registerForPubSub('http://example.com/simple')
        self.registerForPubSub('http://example.com/event#', True)

    def initPubSubAuth(self):
        self.registerForPubSub('http://example.com/event/simple')
        self.topicservice = MyTopicService([1, 3, 7])
        self.registerHandlerForPubSub(self.topicservice, 'http://example.com/event/')


class WampTestServerFactory(WampServerFactory):
    protocol = WampTestServerProtocol

    def __init__(self, url, debug=False):
        WampServerFactory.__init__(self, url, debugWamp=debug)
        self.setProtocolOptions(allowHixie76=True)
        self.keyvalue = KeyValue('keyvalue.dat')
        decimal.getcontext().prec = 20