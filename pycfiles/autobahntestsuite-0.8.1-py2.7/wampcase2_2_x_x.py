# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/wampcase/wampcase2_2_x_x.py
# Compiled at: 2018-12-17 11:51:20
__all__ = [
 'Cases']
Cases = []
import json
from zope.interface import implementer
from twisted.internet import reactor
from twisted.internet.defer import Deferred, DeferredList
from autobahn.twisted.websocket import connectWS
from autobahn.wamp import WampClientFactory, WampCraClientProtocol
from autobahntestsuite.testrun import TestResult
from autobahntestsuite.util import AttributeBag, perf_counter
from autobahntestsuite.interfaces import ITestCase
TOPIC_PUBLISHED_TO = 'http://example.com/simple'
TOPIC_NOT_PUBLISHED_TO = 'http://example.com/foobar'
TOPIC_NOT_REGISTERED = 'http://example.com/barbaz'
PEERSET0_1 = [
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO, TOPIC_NOT_PUBLISHED_TO],
 [
  TOPIC_NOT_PUBLISHED_TO], []]
PEERSET0_2 = [[],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO, TOPIC_NOT_PUBLISHED_TO],
 [
  TOPIC_NOT_PUBLISHED_TO], []]
PEERSET0_3 = [
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO, TOPIC_NOT_PUBLISHED_TO],
 [
  TOPIC_NOT_PUBLISHED_TO], []]
PEERSET0_4 = [
 [
  TOPIC_NOT_REGISTERED],
 [
  TOPIC_NOT_REGISTERED],
 [
  TOPIC_NOT_REGISTERED, TOPIC_NOT_PUBLISHED_TO],
 [
  TOPIC_NOT_PUBLISHED_TO], []]
PEERSET0_5 = [
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO]]
SETTINGS0 = [
 (
  PEERSET0_1, TOPIC_PUBLISHED_TO, None, None, None, [1, 2]),
 (
  PEERSET0_2, TOPIC_PUBLISHED_TO, None, None, None, [1, 2]),
 (
  PEERSET0_3, TOPIC_NOT_REGISTERED, None, None, None, []),
 (
  PEERSET0_4, TOPIC_NOT_REGISTERED, None, None, None, []),
 (
  PEERSET0_5, TOPIC_PUBLISHED_TO, None, None, None, [1, 2, 3, 4, 5, 6, 7, 8, 9])]
PAYLOADS0 = [
 [
  None],
 [
  100],
 [
  -0.248],
 [
  -1000000],
 [
  'hello'],
 [
  True],
 [
  False],
 [
  666, 23, 999], [{}, [], None],
 [
  100, 'hello', {'foo': 'bar'}, [1, 2, 3], ['hello', 20, {'baz': 'poo'}]]]
TOPIC_PUBLISHED_TO = 'http://example.com/simple'
PEERSET1 = [
 [
  TOPIC_PUBLISHED_TO],
 [
  TOPIC_PUBLISHED_TO]]
SETTINGS1 = [
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, None, None, [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, None, None, [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, None, None, [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [], None, [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [], None, [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [], None, [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0], None, [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0], None, [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0], None, [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [1], None, [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [1], None, [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [1], None, [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0, 1], None, []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0, 1], None, []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0, 1], None, []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, None, [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, None, [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, None, [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, None, [0, 1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, None, [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, None, [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, None, [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, None, [0, 1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, None, [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, None, [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, None, [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, None, [0, 1], [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [], [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [], [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [], [0, 1], [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [], [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [], [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [], [0, 1], [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [], [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [], [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [], [0, 1], [0, 1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0], [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0], [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0], [0, 1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0], [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0], [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0], [0, 1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0], [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0], [1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0], [0, 1], [1]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [1], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [1], [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [1], [1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [1], [0, 1], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [1], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [1], [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [1], [1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [1], [0, 1], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [1], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [1], [0], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [1], [1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [1], [0, 1], [0]),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0, 1], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0, 1], [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0, 1], [1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, None, [0, 1], [0, 1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0, 1], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0, 1], [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0, 1], [1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, True, [0, 1], [0, 1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0, 1], [], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0, 1], [0], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0, 1], [1], []),
 (
  PEERSET1, TOPIC_PUBLISHED_TO, False, [0, 1], [0, 1], [])]
PAYLOADS1 = [
 [
  'Hello, world!']]

class WampCase2_2_x_x_Protocol(WampCraClientProtocol):

    def onSessionOpen(self):
        self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, 'WAMP session opened to <strong>%s</strong> at <strong>%s</strong>.' % (self.session_server, self.peer)))
        if self.test.testee.auth:
            d = self.authenticate(**self.test.testee.auth)
            d.addCallbacks(self.onAuthSuccess, self.onAuthError)
        else:
            self.main()

    def sendMessage(self, payload):
        self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, '<pre class="wamp">TX => %s</pre>' % payload))
        WampCraClientProtocol.sendMessage(self, payload)

    def onMessage(self, payload, binary):
        self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, '<pre class="wamp">RX <= %s</pre>' % payload))
        WampCraClientProtocol.onMessage(self, payload, binary)

    def onAuthSuccess(self, permissions):
        self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, 'WAMP session %s authenticated with credentials: <pre>%s</pre>' % (self.session_id, self.test.testee.auth)))
        self.main()

    def onAuthError(self, e):
        uri, desc, details = e.value.args
        self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, 'WAMP authentication error: %s' % details))
        print 'Authentication Error!', uri, desc, details

    def main(self):
        subscribeTopics = self.test.params.peers[self.factory.peerIndex]
        for topic in subscribeTopics:
            topic += self.factory.test._uriSuffix
            self.subscribe(topic, self.onEvent)
            self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, 'Subscribed to <pre>%s</pre>' % topic))

        self.factory.onReady.callback(self.session_id)

    def onEvent(self, topic, event):
        self.test.result.log.append((perf_counter(), self.factory.peerIndex, self.session_id, 'Received event for topic <pre>%s</pre> and payload <pre>%s</pre>' % (topic, event)))
        if not self.test.result.observed.has_key(self.session_id):
            self.test.result.observed[self.session_id] = []
        self.test.result.observed[self.session_id].append((topic, event))


class WampCase2_2_x_x_Factory(WampClientFactory):
    protocol = WampCase2_2_x_x_Protocol

    def __init__(self, test, peerIndex, onReady, onGone):
        WampClientFactory.__init__(self, test.testee.url)
        self.test = test
        self.peerIndex = peerIndex
        self.onReady = onReady
        self.onGone = onGone
        self.proto = None
        return

    def buildProtocol(self, addr):
        proto = self.protocol()
        proto.factory = self
        proto.test = self.test
        proto.session_id = None
        self.proto = proto
        return proto

    def clientConnectionLost(self, connector, reason):
        reason = str(reason.value)
        if self.proto and hasattr(self.proto, 'session_id'):
            sid = self.proto.session_id
        else:
            sid = None
        self.test.result.log.append((perf_counter(), self.peerIndex, sid, 'Client connection lost: %s' % reason))
        self.onGone.callback(None)
        return

    def clientConnectionFailed(self, connector, reason):
        reason = str(reason.value)
        self.test.result.log.append((perf_counter(), self.peerIndex, None, 'Client connection failed: %s' % reason))
        self.onGone.callback(reason)
        return


class WampCase2_2_x_x_Params(AttributeBag):
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
     'publicationMethod',
     'excludeMe',
     'exclude',
     'eligible',
     'eventPayloads',
     'expectedReceivers']


import random

@implementer(ITestCase)
class WampCase2_2_x_x_Base:

    def __init__(self, testee, spec):
        self.testee = testee
        self.spec = spec
        self.result = TestResult()
        self.result.passed = False
        self.result.observed = {}
        self.result.expected = {}
        self.result.log = []
        self._uriSuffix = '#' + str(random.randint(0, 1000000))
        if self.testee.options.has_key('rtt'):
            self._rtt = self.testee.options['rtt']
        elif self.spec.has_key('options') and self.spec['options'].has_key('rtt'):
            self._rtt = self.spec['options']['rtt']
        else:
            self._rtt = 0.2

    def run(self):
        self.result.started = perf_counter()
        self.result.log.append((self.result.started, None, None, 'Test started.'))
        self.clients = []
        peersready = []
        peersgone = []
        i = 1
        for peerIndex in xrange(len(self.params.peers)):
            ready = Deferred()
            gone = Deferred()
            client = WampCase2_2_x_x_Factory(self, peerIndex, ready, gone)
            self.clients.append(client)
            peersready.append(ready)
            peersgone.append(gone)
            connectWS(client)
            i += 1

        def shutdown():
            for c in self.clients:
                c.proto.sendClose()
                self.result.log.append((perf_counter(), c.peerIndex, c.proto.session_id, 'Test client closing ...'))

        def test():
            for c in self.clients:
                self.result.expected[c.proto.session_id] = []
                self.result.observed[c.proto.session_id] = []

            publisherPeerIndex = 0
            publisher = self.clients[publisherPeerIndex]
            publisherSessionId = publisher.proto.session_id
            topic = self.params.publicationTopic + self._uriSuffix
            payloads = self.params.eventPayloads
            expectedReceivers = [ self.clients[i] for i in self.params.expectedReceivers ]
            for r in expectedReceivers:
                for p in payloads:
                    self.result.expected[r.proto.session_id].append((topic, p))

            args = {}
            if self.params.excludeMe is not None:
                args['excludeMe'] = self.params.excludeMe
            if self.params.exclude is not None:
                args['exclude'] = []
                for i in self.params.exclude:
                    args['exclude'].append(self.clients[i].proto.session_id)

            if self.params.eligible is not None:
                args['eligible'] = []
                for i in self.params.eligible:
                    args['eligible'].append(self.clients[i].proto.session_id)

            d_pl = []
            for pl in payloads:
                if self.params.publicationMethod == 0:
                    publisher.proto.publish(topic, pl, **args)
                elif self.params.publicationMethod == 1:
                    args['me'] = publisherSessionId
                    ENDPOINT = 'http://api.testsuite.wamp.ws/testee/control#dispatch'
                    cd = publisher.proto.call(ENDPOINT, topic, pl, args)
                    del args['me']
                    d_pl.append(cd)
                else:
                    raise Exception('no such publication method: %s' % self.params.publicationMethod)
                s_args = [ '%s=%s' % (k, v) for k, v in args.items() ]
                if len(s_args) > 0:
                    s_args = 'with options <pre>%s</pre> ' % (', ').join(s_args)
                else:
                    s_args = ''
                if self.params.publicationMethod == 0:
                    msg = 'Published event to topic <pre>%s</pre> %sand payload <pre>%s</pre>' % (topic, s_args, pl)
                elif self.params.publicationMethod == 1:
                    msg = 'Initiated server dispatched event to topic <pre>%s</pre> %sand payload <pre>%s</pre>' % (topic, s_args, pl)
                else:
                    msg = ''
                self.result.log.append((perf_counter(), publisherPeerIndex, publisher.proto.session_id, msg))

            wait = 1.5 * self._rtt

            def afterwait():
                self.result.log.append((perf_counter(), None, None, 'Continuing test ..'))
                shutdown()
                return

            def beforewait():
                self.result.log.append((perf_counter(), None, None, 'Sleeping for <strong>%s ms</strong> ...' % (1000.0 * wait)))
                reactor.callLater(wait, afterwait)
                return

            if self.params.publicationMethod == 1 and len(d_pl) > 0:
                d = DeferredList(d_pl)

                def onres(res):
                    self.result.log.append((perf_counter(), None, None, 'Event init call result: %s' % res))
                    beforewait()
                    return

                d.addCallback(onres)
            else:
                beforewait()
            return

        def launch(_):
            wait = 2.5 * self._rtt

            def afterwait():
                self.result.log.append((perf_counter(), None, None, 'Continuing test ..'))
                test()
                return

            self.result.log.append((perf_counter(), None, None, 'Sleeping for  <strong>%s ms</strong> ...' % (1000.0 * wait)))

            def beforewait():
                reactor.callLater(wait, afterwait)

            reactor.callLater(0, beforewait)
            return

        def error(err):
            print 'ERROR', err
            shutdown()
            self.finished.errback(err)

        def done(res):
            self.result.ended = perf_counter()
            self.result.log.append((self.result.ended, None, None, 'Test ended.'))
            clientErrors = []
            for r in res:
                if not r[0]:
                    clientErrors.append(str(r[1].value))

            if len(clientErrors) > 0:
                passed = False
                print 'Client errors', clientErrors
            else:
                passed = json.dumps(self.result.observed) == json.dumps(self.result.expected)
                if False and not passed:
                    print
                    print 'EXPECTED'
                    print self.result.expected
                    print 'OBSERVED'
                    print self.result.observed
                    print
            self.result.passed = passed
            self.finished.callback(self.result)
            return

        DeferredList(peersready).addCallbacks(launch, error)
        DeferredList(peersgone).addCallbacks(done, error)
        self.finished = Deferred()
        return self.finished


def generate_WampCase2_2_x_x_classes(baseIndex, settings, payloads, publicationMethod=0):
    res = []
    jc = 1
    for setting in settings:
        ic = 1
        for payload in payloads:
            params = WampCase2_2_x_x_Params(peers=setting[0], publicationTopic=setting[1], publicationMethod=publicationMethod, excludeMe=setting[2], exclude=setting[3], eligible=setting[4], eventPayloads=payload, expectedReceivers=setting[5])
            pl = len(params.eventPayloads)
            plc = 's' if pl else ''
            s = []
            i = 0
            for p in params.peers:
                if len(p) > 0:
                    s.append('<strong>%s</strong>: <i>%s</i>' % (i, (' & ').join(p)))
                else:
                    s.append('<strong>%s</strong>: <i>%s</i>' % (i, '-'))
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
            description = 'The test connects <strong>%s</strong> WAMP clients to the testee, subscribes the sessions to topics %s, waits <strong>3xRTT</strong> seconds and then publishes <strong>%d</strong> event%s to the topic <i>%s</i> with payload%s <i>%s</i> from the first session. The test then waits <strong>3xRTT</strong> seconds to receive events dispatched from the testee.\n<br><br>\nFor publishing of test events, the following publication options are used: <i>%s</i>.\n<br><br>\nNote that the test has used the topic URIs from above description with a session specific suffix, e.g. <i>#6011</i>. See the log for actual URIs used.\n' % (len(params.peers),
             s,
             pl,
             plc,
             params.publicationTopic,
             plc,
             (', ').join([ str(x) for x in params.eventPayloads ]),
             o)
            expectation = 'We expect the testee to dispatch the events to us on the sessions %s' % (', ').join([ '<strong>%s</strong>' % x for x in params.expectedReceivers ])
            index = (
             baseIndex[0], baseIndex[1], jc, ic)
            klassname = 'WampCase%d_%d_%d_%d' % index
            Klass = type(klassname, (
             object, WampCase2_2_x_x_Base), {'__init__': WampCase2_2_x_x_Base.__init__, 
               'run': WampCase2_2_x_x_Base.run, 
               'index': index, 
               'description': description, 
               'expectation': expectation, 
               'params': params})
            res.append(Klass)
            ic += 1

        jc += 1

    return res


Cases.extend(generate_WampCase2_2_x_x_classes((2, 1), SETTINGS0, PAYLOADS0, 0))
Cases.extend(generate_WampCase2_2_x_x_classes((2, 2), SETTINGS0, PAYLOADS0, 0))
Cases.extend(generate_WampCase2_2_x_x_classes((2, 3), SETTINGS1, PAYLOADS1, 1))
Cases.extend(generate_WampCase2_2_x_x_classes((2, 4), SETTINGS1, PAYLOADS1, 1))