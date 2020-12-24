# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/rules/test/test_frequency.py
# Compiled at: 2009-01-30 08:10:10
"""
Тесты на L{spamfighter.rules.frequency}.
"""
from twisted.internet import defer
from twisted.trial import unittest
from spamfighter.utils.time import startUpTestTimer, advanceTestTimer, tearDownTestTimer
from spamfighter.rules.frequency import messageFrequencyCheck, calculateMD5, clearMessage, userFrequencyCheck
from spamfighter.core.message import TransitMessage
from spamfighter.core.domain import getDefaultDomain
from spamfighter.core.storage.memory import DomainMemoryStorage, MemoryStorage

class FrequencyRulesTestCase(unittest.TestCase):
    """
    Тест на L{spamfighter.rules.frequency}.
    """

    def setUp(self):
        getDefaultDomain().set('testStorage', DomainMemoryStorage(storage=MemoryStorage(cleanupInterval=0)))
        self.message1 = TransitMessage(serialized={'text': 'мама мыла раму папы', 'ip': '192.168.140.4'}).getMessage(getDefaultDomain())
        self.message2 = TransitMessage(serialized={'text': 'папа'}).getMessage(getDefaultDomain())
        self.message3 = TransitMessage(serialized={'text': 'привет всем в чате!', 'from': 15}).getMessage(getDefaultDomain())
        self.message4 = TransitMessage(serialized={'text': 'и тебе привет!', 'from': 16, 'ip': '192.168.140.4'}).getMessage(getDefaultDomain())
        startUpTestTimer(1000)

    def tearDown(self):
        getDefaultDomain().delete('testStorage')
        tearDownTestTimer()

    def testCalculateMD5(self):
        self.assertEquals('f6b9cb6316325114b93fc8d32399bece', calculateMD5('мама не помыла раму'))

    def testClearMessage(self):
        self.assertEquals('мамамыламыламыла', clearMessage('Мама мыла, мыла, мыла!!!!'))

    def testFrequencyCheckOneMessage(self):
        return messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage='testStorage', timeout=10, count=2).addCallback(self.assertTrue)

    def testCountMessages(self):
        d = defer.succeed(None)
        for i in xrange(15):
            d.addCallback(lambda _: messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage='testStorage', count=16, timeout=10).addCallback(self.assertTrue))

        d.addCallback(lambda _: messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage='testStorage', count=16, timeout=10).addCallback(self.assertFalse)).addCallback(lambda _: advanceTestTimer(10)).addCallback(lambda _: messageFrequencyCheck(domain=getDefaultDomain(), message=self.message1, storage='testStorage', count=16, timeout=10).addCallback(self.assertTrue))
        return d

    def testFrequencyCheckOneUser(self):
        return messageFrequencyCheck(domain=getDefaultDomain(), message=self.message3, storage='testStorage', timeout=10, count=2).addCallback(self.assertTrue)

    def testCountUserMessages(self):
        d = defer.succeed(None)
        for i in xrange(15):
            d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, storage='testStorage', count=16, timeout=10).addCallback(self.assertTrue))

        d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, storage='testStorage', count=16, timeout=10).addCallback(self.assertFalse)).addCallback(lambda _: advanceTestTimer(10)).addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, storage='testStorage', count=16, timeout=10).addCallback(self.assertTrue))
        return d

    def testCountIPMessages(self):
        d = defer.succeed(None)
        for i in xrange(15):
            d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, attribute='ip', storage='testStorage', count=16, timeout=10).addCallback(self.assertTrue))

        d.addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, attribute='ip', storage='testStorage', count=16, timeout=10).addCallback(self.assertFalse)).addCallback(lambda _: advanceTestTimer(10)).addCallback(lambda _: userFrequencyCheck(domain=getDefaultDomain(), message=self.message4, attribute='ip', storage='testStorage', count=16, timeout=10).addCallback(self.assertTrue))
        return d