# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/wsperfcontrol.py
# Compiled at: 2018-12-17 11:51:20
__all__ = [
 'startClient', 'startServer']
import sys, json, pprint
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, WebSocketClientProtocol, connectWS
from autobahn.util import newid

class WsPerfControlProtocol(WebSocketClientProtocol):
    """
   A client for wsperf running in server mode.

      stress_test:
         token:               Token included in test results.
         uri:                 WebSocket URI of testee.
         handshake_delay:     Delay in ms between opening new WS connections. What about failed connection attempts?
         connection_count:    How many WS connections to open. Definitely opened, or excluding failed?
         con_duration:        How long the WS sits idle before closing the WS. How does that work if msg_count > 0?
         con_lifetime:        ?
         msg_count:           Number of messages per WS connection.
         msg_size:            Size of each message.
         msg_mode:            ?
         ?:                   ? Any other? What about the other parameters available in message_test?
   """
    WSPERF_CMDS = {'echo': 'message_test:uri=%(uri)s;token=%(token)s;size=%(size)d;count=%(count)d;quantile_count=%(quantile_count)d;timeout=%(timeout)d;binary=%(binary)s;sync=%(sync)s;rtts=%(rtts)s;correctness=%(correctness)s;', 'stress': 'stress_test:uri=%(uri)s;token=%(token)s;handshake_delay=%(handshake_delay)d;connection_count=%(connection_count)d;%(con_duration)d;msg_count=%(msg_count)d;msg_size=%(msg_size)d;rtts=%(rtts)s;'}

    def sendNext(self):
        if self.currentTestset == len(self.testsets):
            return True
        else:
            if self.currentTest == len(self.testsets[self.currentTestset][1]):
                self.currentTestset += 1
                self.currentTest = 0
                return self.sendNext()
            test = self.testsets[self.currentTestset][1][self.currentTest]
            cmd = self.WSPERF_CMDS[test['mode']] % test
            if self.factory.debugWsPerf:
                print 'Starting test for testee %s' % test['name']
                print cmd
            sys.stdout.write('.')
            self.sendMessage(cmd)
            self.currentTest += 1
            return False

    def setupTests(self):
        i = 0
        cnt = 0
        for testset in self.factory.spec['testsets']:
            self.testsets.append((testset, []))
            for server in self.factory.spec['servers']:
                for case in testset['cases']:
                    id = newid()
                    if testset['mode'] == 'echo':
                        test = {'token': id, 'mode': testset['mode'], 
                           'uri': server['uri'].encode('utf8'), 
                           'name': server['name'].encode('utf8'), 
                           'quantile_count': testset['options']['quantile_count'], 
                           'rtts': 'true' if testset['options']['rtts'] else 'false', 
                           'count': case['count'] if case.has_key('count') else testset['options']['count'], 
                           'size': case['size'] if case.has_key('size') else testset['options']['size'], 
                           'timeout': case['timeout'] if case.has_key('timeout') else testset['options']['timeout'], 
                           'binary': 'true' if case['binary'] if case.has_key('binary') else testset['options']['binary'] else 'false', 
                           'sync': 'true' if case['sync'] if case.has_key('sync') else testset['options']['sync'] else 'false', 
                           'correctness': 'exact' if case['verify'] if case.has_key('verify') else testset['options']['verify'] else 'length', 
                           'count': case['count'] if case.has_key('count') else testset['options']['count']}
                    else:
                        raise Exception('unknown mode %s' % testset['mode'])
                    self.testsets[i][1].append(test)
                    cnt += 1

            i += 1

        sys.stdout.write('Running %d tests in total against %d servers: ' % (cnt, len(self.factory.spec['servers'])))

    def toMicroSec(self, value, digits=0):
        return ('%.' + str(digits) + 'f') % round(float(value), digits)

    def getMicroSec(self, result, field, digits=0):
        return self.toMicroSec(result['data'][field], digits)

    def onTestsComplete(self):
        print ' All tests finished.'
        print
        if self.factory.debugWsPerf:
            self.pp.pprint(self.testresults)
        for testset in self.testsets:
            if testset[0]['options'].has_key('outfile'):
                outfilename = testset[0]['options']['outfile']
                outfile = open(outfilename, 'w')
            else:
                outfilename = None
                outfile = sys.stdout
            if testset[0]['options'].has_key('digits'):
                digits = testset[0]['options']['digits']
            else:
                digits = 0
            if testset[0]['options'].has_key('sep'):
                sep = testset[0]['options']['sep']
            else:
                sep = '\t'
            if testset[0]['mode'] == 'echo':
                outfile.write(sep.join(['name', 'outcome', 'count', 'size', 'min', 'median', 'max', 'avg', 'stddev']))
                quantile_count = testset[0]['options']['quantile_count']
                for i in xrange(quantile_count):
                    outfile.write(sep)
                    outfile.write('q%d' % i)

                outfile.write('\n')
                for test in testset[1]:
                    result = self.testresults[test['token']]
                    outcome = result['data']['result']
                    if outcome == 'connection_failed':
                        outfile.write(sep.join([test['name'], 'UNREACHABLE']))
                        outfile.write('\n')
                    elif outcome == 'time_out':
                        outfile.write(sep.join([test['name'], 'TIMEOUT']))
                        outfile.write('\n')
                    elif outcome == 'fail':
                        outfile.write(sep.join([test['name'], 'FAILED']))
                        outfile.write('\n')
                    elif outcome == 'pass':
                        outfile.write(sep.join([ str(x) for x in [test['name'],
                         'PASSED',
                         test['count'],
                         test['size'],
                         self.getMicroSec(result, 'min', digits),
                         self.getMicroSec(result, 'median', digits),
                         self.getMicroSec(result, 'max', digits),
                         self.getMicroSec(result, 'avg', digits),
                         self.getMicroSec(result, 'stddev', digits)]
                                               ]))
                        for i in xrange(quantile_count):
                            outfile.write(sep)
                            if result['data'].has_key('quantiles'):
                                outfile.write(self.toMicroSec(result['data']['quantiles'][i][1]))

                        outfile.write('\n')
                    else:
                        raise Exception("unknown case outcome '%s'" % outcome)

                if outfilename:
                    print 'Test data written to %s.' % outfilename
            else:
                raise Exception('logic error')

        reactor.stop()
        return

    def onOpen(self):
        self.pp = pprint.PrettyPrinter(indent=3)
        self.testresults = {}
        self.testsets = []
        self.currentTestset = 0
        self.currentTest = 0
        self.setupTests()
        self.sendNext()

    def onMessage(self, msg, binary):
        if not binary:
            try:
                o = json.loads(msg)
                if o['type'] == 'test_complete':
                    if self.sendNext():
                        self.onTestsComplete()
                elif o['type'] == 'test_data':
                    if self.factory.debugWsPerf:
                        self.pp.pprint(o)
                    self.testresults[o['token']] = o
            except ValueError as e:
                pass


class WsPerfControlFactory(WebSocketClientFactory):
    protocol = WsPerfControlProtocol


def startClient(wsuri, spec, debug=False):
    factory = WsPerfControlFactory(wsuri)
    factory.spec = spec
    factory.debugWsPerf = spec['options']['debug']
    connectWS(factory)
    return True