# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/wampcase/wampcase3_1_x_x.py
# Compiled at: 2018-12-17 11:51:20
__all__ = [
 'Cases']
Cases = []
import json, time
from zope.interface import implementer
from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList, maybeDeferred
from autobahn.twisted.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampCraClientProtocol
from autobahntestsuite.testrun import TestResult
from autobahntestsuite.util import AttributeBag, perf_counter
from autobahntestsuite.interfaces import ITestCase

class WampCase3_1_x_x_Protocol(WampCraClientProtocol):

    def onSessionOpen(self):
        if self.test.testee.auth:
            d = self.authenticate(**self.test.testee.auth)
            d.addCallbacks(self.onAuthSuccess, self.onAuthError)
        else:
            self.main()

    def onAuthSuccess(self, permissions):
        self.main()

    def onAuthError(self, e):
        uri, desc, details = e.value.args
        print 'Authentication Error!', uri, desc, details

    def main(self):
        self.factory.onReady(self)


class WampCase3_1_x_x_Factory(WampClientFactory):
    protocol = WampCase3_1_x_x_Protocol

    def __init__(self, test, onReady, onGone):
        WampClientFactory.__init__(self, test.testee.url)
        self.test = test
        self.onReady = onReady
        self.onGone = onGone
        self.proto = None
        return

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.factory = self
        proto.test = self.test
        self.proto = proto
        return proto

    def clientConnectionLost(self, connector, reason):
        self.onGone(self.proto)

    def clientConnectionFailed(self, connector, reason):
        self.onGone(self.proto)


class WampCase3_1_x_x_Params(AttributeBag):
    """
   Test parameter set for configuring instances of WampCase2_*_*.

   peers: a list with one item per WAMP session run during the test, where each item contains a list of topics each peer _subscribes_ to. The publisher that publishes during the test is always the first item in the list.

   publicationTopic, excludeMe, exclude, eligible: parameters controlling how events are published during the test.

   eventPayloads: a list of payloads each tested as event payload to the test at hand.

   expectedReceivers: a list of session indices, where each index references a WAMP session created for the list in `peers`.
   """
    ATTRIBUTES = [
     'peers',
     'publicationTopic',
     'excludeMe',
     'exclude',
     'eligible',
     'eventPayloads',
     'expectedReceivers']


@implementer(ITestCase)
class WampCase3_1_x_x_Base:
    DESCRIPTION = 'Undefined.'
    EXPECTATION = 'Undefined.'

    def __init__(self, testee):
        self.testee = testee
        self.client = None
        self.result = TestResult()
        self.result.received = {}
        self.result.expected = {}
        self.result.log = []
        return

    def run(self):
        self.result.started = perf_counter()

        def shutdown():
            if self.client:
                self.client.proto.sendClose()

        def test(proto):

            def perform(i, p):
                d = proto.call('http://api.testsuite.wamp.ws/case/3.1.1#1', float(p))

                def got(res):
                    self.result.received[i] = float(res)

                d.addCallback(got)

            payloads = []
            payloads.extend([0])
            payloads.extend([127, 255, 32767, 65535, 16777216])
            payloads.extend([-128, -32768, -16777216])
            i = 0
            for p in payloads:
                self.result.expected[i] = float(p)
                perform(i, p)
                i += 1

            wait = 3 * self.testee.options.get('rtt', 0.2)
            reactor.callLater(wait, shutdown)

        def launch(proto):
            reactor.callLater(1e-05, test, proto)

        def error(err):
            print 'ERROR', err
            shutdown()
            self.finished.errback(err)

        def done(proto):
            self.result.ended = perf_counter()
            passed = json.dumps(self.result.received) == json.dumps(self.result.expected)
            if not passed:
                print 'EXPECTED', self.result.expected
                print 'RECEIVED', self.result.received
            self.result.passed = passed
            self.finished.callback(self.result)

        self.client = WampCase3_1_x_x_Factory(self, launch, done)
        connectWS(self.client)
        self.finished = Deferred()
        return self.finished


class WampCase3_1_1_1(WampCase3_1_x_x_Base):
    pass


Cases = [
 WampCase3_1_1_1]

def generate_WampCase3_1_x_x_classes2():
    res = []
    jc = 1
    for setting in SETTINGS:
        ic = 1
        for payload in PAYLOADS:
            params = WampCase2_2_x_x_Params(peers=setting[0], publicationTopic=setting[1], excludeMe=setting[2], exclude=setting[3], eligible=setting[4], eventPayloads=payload, expectedReceivers=setting[5])
            pl = len(params.eventPayloads)
            plc = 's' if pl else ''
            s = []
            i = 0
            for p in params.peers:
                if len(p) > 0:
                    s.append('%d: %s' % (i, (' & ').join(p)))
                else:
                    s.append('%d: %s' % (i, '-'))
                i += 1

            s = (', ').join(s)
            o = []
            if params.excludeMe is not None:
                o.append('excludeMe = %s' % params.excludeMe)
            if params.exclude is not None:
                o.append('exclude = %s' % params.exclude)
            if params.eligible is not None:
                o.append('eligible = %s' % params.eligible)
            if len(o) > 0:
                o = (', ').join(o)
            else:
                o = '-'
            description = 'The test connects %d WAMP clients to the testee, subscribes the sessions to topics %s and then publishes %d event%s to the topic %s with payload%s %s from the first session. The test sets the following publication options: %s.\n' % (len(params.peers),
             s,
             pl,
             plc,
             params.publicationTopic,
             plc,
             (', ').join([ '"' + str(x) + '"' for x in params.eventPayloads ]),
             o)
            expectation = 'We expect the testee to dispatch the events to us on the sessions %s' % (params.expectedReceivers,)
            klassname = 'WampCase3_1_%d_%d' % (jc, ic)
            Klass = type(klassname, (
             object, WampCase3_1_x_x_Base), {'__init__': WampCase3_1_x_x_Base.__init__, 
               'run': WampCase3_1_x_x_Base.run, 
               'description': description, 
               'expectation': expectation, 
               'params': params})
            res.append(Klass)
            ic += 1

        jc += 1

    return res