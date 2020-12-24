# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/ooni/nettests/blocking/meek_fronted_requests.py
# Compiled at: 2017-04-04 12:48:22
from twisted.python import usage
from ooni.templates import httpt
from ooni.utils import log

class UsageOptions(usage.Options):
    optParameters = [
     [
      'expectedBody', 'B',
      'I’m just a happy little web server.\n',
      'Expected body content from GET response.'],
     [
      'domainName', 'D', None,
      'Specify a single fronted domainName to test.'],
     [
      'hostHeader', 'H', None,
      'Specify "inside" Host Header to test.']]


class meekTest(httpt.HTTPTest):
    """
    Performs a HTTP GET request to a list of fronted domains with the Host
    Header of the "inside" meek-server. The meek-server handles a GET request
    and response with: "I’m just a happy little web server.
".
    The input file should be formatted as (one per line):
    "domainName:hostHeader"
    ajax.aspnetcdn.com:az668014.vo.msecnd.net
    a0.awsstatic.com:d2zfqthxsdq309.cloudfront.net

    """
    name = 'Meek fronted requests test'
    description = 'This test examines whether the domains used by Meek (a type of Tor bridge) work in your network.'
    version = '0.1.0'
    usageOptions = UsageOptions
    inputFile = ['file', 'f', None,
     'File containing the domainName:hostHeader combinations to                  be tested, one per line.']
    inputs = [('ajax.aspnetcdn.com', 'az668014.vo.msecnd.net'),
     ('a0.awsstatic.com', 'd2zfqthxsdq309.cloudfront.net')]
    requiresRoot = False
    requiresTor = False

    def setUp(self):
        """
        Check for inputs.
        """
        if self.input:
            if isinstance(self.input, tuple) or isinstance(self.input, list):
                self.domainName, self.header = self.input
            else:
                self.domainName, self.header = self.input.split(':')
        elif self.localOptions['domainName'] and self.localOptions['hostHeader']:
            self.domainName = self.localOptions['domainName']
            self.header = self.localOptions['hostHeader']
        self.expectedBody = self.localOptions['expectedBody']
        self.domainName = 'https://' + self.domainName

    def test_meek_response(self):
        """
        Detects if the fronted request is blocked.
        """
        log.msg('Testing fronted domain:%s with Host Header:%s' % (
         self.domainName, self.header))

        def process_body(body):
            if self.expectedBody != body:
                self.report['success'] = False
            else:
                self.report['success'] = True

        headers = {}
        headers['Host'] = [self.header]
        return self.doRequest(self.domainName, method='GET', headers=headers, body_processor=process_body)