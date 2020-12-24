# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x/code/OONI/ooni-probe/docs/source/../../ooni/nettests/experimental/domclass_collector.py
# Compiled at: 2017-04-04 12:48:22
from ooni.kit import domclass
from ooni.templates import httpt

class DOMClassCollector(httpt.HTTPTest):
    name = 'DOM class collector'
    author = 'Arturo Filastò'
    version = '0.2.0'
    followRedirects = True
    inputFile = [
     'file', 'f', None, 'The list of urls to build a domclass for']
    requiresTor = False
    requiresRoot = False

    def test_collect(self):
        if self.input:
            url = self.input
            return self.doRequest(url)
        raise Exception('No input specified')

    def processResponseBody(self, body):
        eigenvalues = domclass.compute_eigenvalues_from_DOM(content=body)
        self.report['eigenvalues'] = eigenvalues.tolist()