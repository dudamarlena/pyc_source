# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/ooni/nettests/experimental/mk_http_invalid_request_line.py
# Compiled at: 2016-09-30 20:40:55
from ooni.templates import mk
from ooni.utils import log
from twisted.python import usage

class UsageOptions(usage.Options):
    optParameters = [
     [
      'backend', 'b', None, 'The OONI backend that runs a TCP echo server.'],
     [
      'backendport', 'p', 80, 'Specify the port that the TCP echo server is running (should only be set for debugging).']]


class MKHTTPInvalidRequestLine(mk.MKTest):
    name = 'HTTP Invalid Request Line'
    version = '0.1.0'
    usageOptions = UsageOptions
    requiresRoot = False
    requiresTor = False
    requiredOptions = [
     'backend']
    requiredTestHelpers = {'backend': 'tcp-echo'}

    def test_run(self):
        log.msg('Running http invalid request line')
        options = {'backend': 'http://' + self.localOptions['backend'] + '/'}
        return self.run('HttpInvalidRequestLine', options)