# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/cases/_test_transfer.py
# Compiled at: 2010-10-16 18:26:43
import random
from twisted.internet.defer import DeferredList, gatherResults, inlineCallbacks, returnValue
from twisted.internet.task import Cooperator
from twisted.python import log
from twisted.trial.unittest import TestCase
from pendrell import messages
from pendrell.cases.junk_server import JunkSiteTestMixin
from pendrell.cases.util import PendrellTestMixin

class _Response(messages.Response):

    def __init__(self, *args, **kw):
        messages.Response.__init__(self, *args, **kw)
        self.count = long()

    def __len__(self):
        return self.count

    def handleData(self, data):
        self.count += len(data)


class _Request(messages.Request):
    responseClass = _Response


class TransferTestMixin(JunkSiteTestMixin):
    chunkSize = 65536
    timeout = 300

    def test_0001xB000(self):
        return self._test_getJunk(0, 'B')

    def test_0001xKB001(self):
        return self._test_getJunk(1, 'KB')

    def test_0001xMB001(self):
        return self._test_getJunk(1, 'MB')

    def test_0002xKB001(self):
        return self._test_getJunks(2, 1, 'KB')

    def test_0016xMB001_0016xKB001(self):
        reqs = [ self._test_getJunk(1, 'MB') for i in xrange(0, 16) ] + [ self._test_getJunk(1, 'KB') for i in xrange(0, 16) ]
        random.shuffle(reqs)
        return gatherResults(reqs)

    def test_0512xKB256(self):
        return self._test_getJunks(512, 256, 'KB')


class XXLTransferTestMixin(JunkSiteTestMixin):
    chunkSize = 65536
    timeout = 2700

    def test_0002xGB1(self):
        return self._test_getJunks(2, 1, 'GB')

    def test_0001xGB4(self):
        return self._test_getJunk(4, 'GB')

    def test_1024xMB001(self):
        return self._test_getJunks(1024, 1, 'MB')


class TransferTest(PendrellTestMixin, TransferTestMixin, TestCase):
    timeout = TransferTestMixin.timeout

    def setUp(self):
        PendrellTestMixin.setUp(self)
        TransferTestMixin.setUp(self)

    @inlineCallbacks
    def tearDown(self):
        yield TransferTestMixin.tearDown(self)
        yield PendrellTestMixin.tearDown(self)

    def getPage(self, url):
        return PendrellTestMixin.getPage(self, _Request(url))


class XXLTransferTest(PendrellTestMixin, XXLTransferTestMixin, TestCase):
    timeout = XXLTransferTestMixin.timeout

    def setUp(self):
        PendrellTestMixin.setUp(self)
        XXLTransferTestMixin.setUp(self)

    @inlineCallbacks
    def tearDown(self):
        yield XXLTransferTestMixin.tearDown(self)
        yield PendrellTestMixin.tearDown(self)

    def getPage(self, url):
        return PendrellTestMixin.getPage(self, _Request(url))