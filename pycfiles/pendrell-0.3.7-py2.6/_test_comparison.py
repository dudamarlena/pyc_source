# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pendrell/cases/_test_comparison.py
# Compiled at: 2010-10-16 18:02:53
from urllib2 import urlopen
from twisted.internet import reactor
from twisted.internet.defer import DeferredSemaphore, gatherResults, inlineCallbacks, maybeDeferred, returnValue, succeed
from twisted.internet.task import Cooperator
from twisted.internet.threads import deferToThread
from twisted.trial.unittest import TestCase
from twisted.web.client import getPage as tx_getPage
from pendrell import log
from pendrell.cases._test_transfer import TransferTestMixin

class ThreadedUrllib2TestMixin(object):

    def setUp(self):
        self._semaphore = DeferredSemaphore(2)

    def tearDown(self):
        pass

    def getPages(self, count, url):
        return gatherResults([ self.getPage(url) for i in xrange(0, count) ])

    @inlineCallbacks
    def getPage(self, url):
        yield self._semaphore.acquire()
        page = yield deferToThread(self._openPage, url)
        self._semaphore.release()
        returnValue(page)

    def _openPage(self, url):
        log.msg('Opening url: %r' % url)
        return urlopen(url).read()

    @inlineCallbacks
    def getPageLength(self, url):
        response = yield self.getPage(url)
        returnValue(len(response))


class TwistedWebTestMixin(object):

    def setUp(self):
        self._semaphore = DeferredSemaphore(2)

    def tearDown(self):
        pass

    @inlineCallbacks
    def getPages(self, count, url):
        return gatherResults([ self.getPage(url) for i in xrange(0, count) ])

    @inlineCallbacks
    def getPage(self, url):
        yield self._semaphore.acquire()
        page = yield tx_getPage(url)
        self._semaphore.release()
        returnValue(page)

    @inlineCallbacks
    def getPageLength(self, url):
        response = yield self.getPage(url)
        returnValue(len(response))


class ThreadedUrllib2TransferTest(TransferTestMixin, ThreadedUrllib2TestMixin, TestCase):
    timeout = 300

    def setUp(self):
        ThreadedUrllib2TestMixin.setUp(self)
        return TransferTestMixin.setUp(self)


class TwistedWebTransferTest(TransferTestMixin, TwistedWebTestMixin, TestCase):
    timeout = 300

    def setUp(self):
        TwistedWebTestMixin.setUp(self)
        return TransferTestMixin.setUp(self)