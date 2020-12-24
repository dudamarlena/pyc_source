# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/third_party/psiphon.py
# Compiled at: 2017-04-04 12:48:22
import tempfile, os, sys
from twisted.internet import defer, reactor
from twisted.internet.error import ProcessExitedAlready
from twisted.python import usage
from ooni.utils import log, net
from ooni.templates import process, httpt

class UsageOptions(usage.Options):
    optParameters = [
     [
      'psiphonpath', 'p', None, 'Specify psiphon python client path.'],
     [
      'url', 'u', net.GOOGLE_HUMANS[0],
      'Specify the URL to fetch over psiphon (default: http://www.google.com/humans.txt).'],
     [
      'expected-body', 'e', net.GOOGLE_HUMANS[1],
      'Specify the beginning of the expected body in the response (default: ' + net.GOOGLE_HUMANS[1] + ').']]


class PsiphonTest(httpt.HTTPTest, process.ProcessTest):
    """
    This class tests Psiphon python client

    test_psiphon:
      Starts a Psiphon, check if it bootstraps successfully
      (print a line in stdout).
      Then, perform an HTTP request using the proxy
    """
    name = 'Psiphon Test'
    description = 'Bootstraps Psiphon and does a HTTP GET for the specified URL.'
    author = 'juga'
    version = '0.2.0'
    timeout = 120
    usageOptions = UsageOptions

    def _setUp(self):
        self.localOptions['socksproxy'] = '127.0.0.1:1080'
        super(PsiphonTest, self)._setUp()

    def setUp(self):
        log.debug('PsiphonTest.setUp')
        self.report['bootstrapped_success'] = None
        self.report['request_success'] = None
        self.report['psiphon_found'] = None
        self.report['default_configuration'] = True
        self.bootstrapped = defer.Deferred()
        self.url = self.localOptions['url']
        if self.localOptions['url'] != net.GOOGLE_HUMANS[0]:
            self.report['default_configuration'] = False
        if self.localOptions['expected-body'] != net.GOOGLE_HUMANS[1]:
            self.report['default_configuration'] = False
        if self.localOptions['psiphonpath']:
            self.psiphonpath = self.localOptions['psiphonpath']
        else:
            from os import path, getenv
            self.psiphonpath = path.join(getenv('HOME'), 'psiphon-circumvention-system/pyclient/pyclient')
            log.debug('psiphon path: %s' % self.psiphonpath)
        return

    def createCommand(self):
        x = '\nfrom psi_client import connect\nconnect(False)\n'
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(x)
        f.close()
        self.command = [sys.executable, f.name]
        log.debug('command: %s' % (' ').join(self.command))

    def handleRead(self, stdout, stderr):
        if 'Press Ctrl-C to terminate.' in self.processDirector.stdout:
            if not self.bootstrapped.called:
                self.report['bootstrapped_success'] = True
                log.debug('PsiphonTest: calling bootstrapped.callback')
                self.bootstrapped.callback(None)
        return

    def test_psiphon(self):
        log.debug('PsiphonTest.test_psiphon')
        self.createCommand()
        if not os.path.exists(self.psiphonpath):
            log.err('psiphon path does not exists, is it installed?')
            self.report['psiphon_found'] = False
            log.debug('Adding %s to report' % self.report)
            reactor.callLater(0.0, self.bootstrapped.callback, None)
            return self.bootstrapped
        else:
            self.report['psiphon_found'] = True
            log.debug('Adding %s to report' % self.report)
            finished = self.run(self.command, env=dict(PYTHONPATH=self.psiphonpath), path=self.psiphonpath, usePTY=1)
            self.report['bootstrapped_success'] = False

            def callDoRequest(_):
                log.debug('PsiphonTest.callDoRequest: %r' % (_,))
                d = self.doRequest(self.url)

                def addSuccessToReport(res):
                    log.debug('PsiphonTest.callDoRequest.addSuccessToReport')
                    if res.body.startswith(self.localOptions['expected-body']):
                        self.report['request_success'] = True
                    else:
                        self.report['request_success'] = False
                    return res

                d.addCallback(addSuccessToReport)

                def addFailureToReport(res):
                    log.debug('PsiphonTest.callDoRequest.addFailureToReport. res=%r' % (res,))
                    self.report['request_success'] = False
                    return res

                d.addErrback(addFailureToReport)
                return d

            self.bootstrapped.addCallback(callDoRequest)

            def cleanup(_):
                log.debug('PsiphonTest:cleanup')
                try:
                    self.processDirector.transport.signalProcess('INT')
                except ProcessExitedAlready:
                    pass

                os.remove(self.command[1])
                return finished

            self.bootstrapped.addBoth(cleanup)
            return self.bootstrapped