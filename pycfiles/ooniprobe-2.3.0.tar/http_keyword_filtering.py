# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/experimental/http_keyword_filtering.py
# Compiled at: 2017-04-04 12:48:22
from twisted.python import usage
from ooni.templates import httpt

class UsageOptions(usage.Options):
    optParameters = [
     [
      'backend', 'b', 'http://127.0.0.1:57001',
      'URL of the test backend to use']]


class HTTPKeywordFiltering(httpt.HTTPTest):
    """
    This test involves performing HTTP requests containing to be tested for
    censorship keywords.

    It does not detect censorship on the client, but just logs the response from the 
    HTTP backend server.
    """
    name = 'HTTP Keyword Filtering'
    author = 'Arturo Filastò'
    version = '0.2.0'
    inputFile = [
     'file', 'f', None, 'List of keywords to use for censorship testing']
    usageOptions = UsageOptions
    requiresTor = False
    requiresRoot = False
    requiredOptions = [
     'backend']

    def test_get(self):
        """
        Perform a HTTP GET request to the backend containing the keyword to be
        tested inside of the request body.
        """
        return self.doRequest(self.localOptions['backend'], method='GET', body=self.input)

    def test_post(self):
        """
        Perform a HTTP POST request to the backend containing the keyword to be
        tested inside of the request body.
        """
        return self.doRequest(self.localOptions['backend'], method='POST', body=self.input)