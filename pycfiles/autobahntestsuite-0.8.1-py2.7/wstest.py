# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/wstest.py
# Compiled at: 2018-12-17 11:51:20
import choosereactor, os, json, sys, pkg_resources
from twisted.internet import reactor
from twisted.python import log, usage
from twisted.internet.defer import Deferred
import autobahn, autobahntestsuite
from autobahn.websocket.utf8validator import Utf8Validator
from autobahn.websocket.xormasker import XorMaskerNull
import testee, fuzzing, echo, broadcast, massconnect, serializer
from spectemplate import SPEC_FUZZINGSERVER, SPEC_FUZZINGCLIENT, SPEC_FUZZINGWAMPSERVER, SPEC_FUZZINGWAMPCLIENT, SPEC_WSPERFCONTROL, SPEC_MASSCONNECT

class WsTestOptions(usage.Options):
    """
   Reads options from the command-line and checks them for plausibility.
   """
    MODES = [
     'echoserver',
     'echoclient',
     'broadcastclient',
     'broadcastserver',
     'fuzzingserver',
     'fuzzingclient',
     'testeeserver',
     'testeeclient',
     'massconnect',
     'serializer']
    MODES_NEEDING_SPEC = [
     'fuzzingclient',
     'fuzzingserver',
     'fuzzingwampserver',
     'fuzzingwampclient',
     'wsperfcontrol',
     'massconnect',
     'import']
    MODES_NEEDING_WSURI = [
     'echoclient',
     'echoserver',
     'broadcastclient',
     'broadcastserver',
     'testeeclient',
     'testeeserver',
     'wsperfcontrol',
     'wampserver',
     'wampclient',
     'wamptesteeserver']
    DEFAULT_SPECIFICATIONS = {'fuzzingclient': SPEC_FUZZINGCLIENT, 'fuzzingserver': SPEC_FUZZINGSERVER, 
       'wsperfcontrol': SPEC_WSPERFCONTROL, 
       'massconnect': SPEC_MASSCONNECT, 
       'fuzzingwampclient': SPEC_FUZZINGWAMPCLIENT, 
       'fuzzingwampserver': SPEC_FUZZINGWAMPSERVER}
    optParameters = [
     [
      'mode', 'm', None, 'Test mode, one of: %s [required]' % (', ').join(MODES)],
     [
      'testset', 't', None, 'Run a test set from an import test spec.'],
     [
      'spec', 's', None, 'Test specification file [required in some modes].'],
     [
      'outfile', 'o', None, 'Output filename for modes that generate testdata.'],
     [
      'wsuri', 'w', None, 'WebSocket URI [required in some modes].'],
     [
      'webport', 'u', 8080, 'Web port for running an embedded HTTP Web server; defaults to 8080; set to 0 to disable. [optionally used in some modes: fuzzingserver, echoserver, broadcastserver, wsperfmaster].'],
     [
      'ident', 'i', None, 'Testee client identifier [optional for client testees].'],
     [
      'key', 'k', None, 'Server private key file for secure WebSocket (WSS) [required in server modes for WSS].'],
     [
      'cert', 'c', None, 'Server certificate file for secure WebSocket (WSS) [required in server modes for WSS].']]
    optFlags = [
     [
      'debug', 'd', 'Debug output [default: off].'],
     [
      'autobahnversion', 'a', 'Print version information for Autobahn and AutobahnTestSuite.']]

    def postOptions(self):
        """
      Process the given options. Perform plausibility checks, etc...
      """
        if self['autobahnversion']:
            print 'Autobahn %s' % autobahn.version
            print 'AutobahnTestSuite %s' % autobahntestsuite.version
            sys.exit(0)
        if not self['mode']:
            raise usage.UsageError, 'a mode must be specified to run!'
        if self['mode'] not in WsTestOptions.MODES:
            raise usage.UsageError, "Mode '%s' is invalid.\nAvailable modes:\n\t- %s" % (
             self['mode'], ('\n\t- ').join(sorted(WsTestOptions.MODES)))
        if self['mode'] in WsTestOptions.MODES_NEEDING_WSURI and not self['wsuri']:
            raise usage.UsageError, 'mode needs a WebSocket URI!'
        if self['webport'] is not None:
            try:
                self['webport'] = int(self['webport'])
                if self['webport'] < 0 or self['webport'] > 65535:
                    raise ValueError()
            except:
                raise usage.UsageError, 'invalid Web port %s' % self['webport']

        return


class WsTestRunner(object):
    """
   Testsuite driver.
   """

    def __init__(self, options, spec=None):
        self.options = options
        self.spec = spec
        self.debug = self.options.get('debug', False)
        if self.debug:
            log.startLogging(sys.stdout)
        self.mode = str(self.options['mode'])

    def startService(self):
        """
      Start mode specific services.
      """
        print
        print 'Using Twisted reactor class %s' % str(reactor.__class__)
        print 'Using UTF8 Validator class %s' % str(Utf8Validator)
        print 'Using XOR Masker classes %s' % str(XorMaskerNull)
        print
        if self.mode == 'import':
            return self.startImportSpec(self.options['spec'])
        else:
            if self.mode == 'export':
                return self.startExportSpec(self.options['testset'], self.options.get('spec', None))
            if self.mode == 'fuzzingwampclient':
                return self.startFuzzingWampClient(self.options['testset'])
            if self.mode == 'web':
                return self.startWeb(debug=self.debug)
            if self.mode == 'testeeclient':
                return testee.startClient(self.options['wsuri'], ident=self.options['ident'], debug=self.debug)
            if self.mode == 'testeeserver':
                return testee.startServer(self.options['wsuri'], debug=self.debug)
            if self.mode == 'broadcastclient':
                return broadcast.startClient(self.options['wsuri'], debug=self.debug)
            if self.mode == 'broadcastserver':
                return broadcast.startServer(self.options['wsuri'], self.options['webport'], debug=self.debug)
            if self.mode == 'echoclient':
                return echo.startClient(self.options['wsuri'], debug=self.debug)
            if self.mode == 'echoserver':
                return echo.startServer(self.options['wsuri'], self.options['webport'], debug=self.debug)
            if self.mode == 'fuzzingclient':
                servers = self.spec.get('servers', [])
                if len(servers) == 0:
                    self.spec['servers'] = [{'url': self.options['wsuri']}]
                return fuzzing.startClient(self.spec, debug=self.debug)
            if self.mode == 'fuzzingserver':
                return fuzzing.startServer(self.spec, self.options['webport'], debug=self.debug)
            if self.mode == 'wsperfcontrol':
                return wsperfcontrol.startClient(self.options['wsuri'], self.spec, debug=self.debug)
            if self.mode == 'wsperfmaster':
                return wsperfmaster.startServer(self.options['webport'], debug=self.debug)
            if self.mode == 'massconnect':
                return massconnect.startClient(self.spec, debug=self.debug)
            if self.mode == 'serializer':
                return serializer.start(outfilename=self.options['outfile'], debug=self.debug)
            raise Exception("no mode '%s'" % self.mode)
            return


def start(options, spec=None):
    """
   Actually startup a wstest run.

   :param options: Global options controlling wstest.
   :type options: dict
   :param spec: Test specification needed for certain modes. If none is given, but
                a spec is needed, a default spec is used.
   :type spec: dict
   """
    if options['mode'] in WsTestOptions.MODES_NEEDING_SPEC and spec is None:
        spec = json.loads(WsTestOptions.DEFAULT_SPECIFICATIONS[options['mode']])
    wstest = WsTestRunner(options, spec)
    res = wstest.startService()
    if res:
        if isinstance(res, Deferred):

            def shutdown(_):
                reactor.stop()

            res.addBoth(shutdown)
        reactor.run()
    return


def run():
    """
   Run wstest from command line. This parses command line args etc.
   """
    cmdOpts = WsTestOptions()
    try:
        cmdOpts.parseOptions()
    except usage.UsageError as errortext:
        print '%s %s\n' % (sys.argv[0], errortext)
        print 'Try %s --help for usage details\n' % sys.argv[0]
        sys.exit(1)
    else:
        options = cmdOpts.opts

    if options['mode'] in WsTestOptions.MODES_NEEDING_SPEC:
        if not options['spec']:
            filename = '%s.json' % options['mode']
            options['spec'] = filename
            if not os.path.isfile(filename):
                content = WsTestOptions.DEFAULT_SPECIFICATIONS[options['mode']]
                print "Auto-generating spec file '%s'" % filename
                f = open(filename, 'w')
                f.write(content)
                f.close()
            else:
                print "Using implicit spec file '%s'" % filename
        else:
            print "Using explicit spec file '%s'" % options['spec']
        spec_filename = os.path.abspath(options['spec'])
        print 'Loading spec from %s' % spec_filename
        spec = json.loads(open(spec_filename).read())
    else:
        spec = None
    start(options, spec)
    return


if __name__ == '__main__':
    run()