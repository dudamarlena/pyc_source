# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spamfighter/plugins/sample_domain_provider.py
# Compiled at: 2009-01-30 08:10:10
"""
Плагин, реализующий корневой домен в качестве возможного примера организации.
"""
from zope.interface import implements
from twisted.plugin import IPlugin
from spamfighter.plugin import IDefaultDomainProvider

class SampleDomainProvider(object):
    """
    Провайдер статического дефолтного домена.
    """
    implements(IPlugin, IDefaultDomainProvider)

    def __init__(self):
        u"""
        Конструктор.
        """
        pass

    def name(self):
        u"""
        Получить имя плагина.

        @return: имя плагина
        @rtype: C{str}
        """
        return 'SampleDomainProvider'

    def getDefaultDomain(self):
        u"""
        Получить домен по умолчанию в системе.

        @return: домен по умолчанию.
        @rtype: L{spamfighter.interfaces.IDomain}
        """
        from spamfighter.core.domain import BaseDomain, getDefaultDomain
        from spamfighter.core.firewall import MessageFirewall
        from spamfighter.core.model.bayes import BayesModel
        from spamfighter.core.message import MessageDomain, TextAttributeDomain, UniqueIntAttributeDomain, IPAttributeDomain
        from spamfighter.core.storage.memory import DomainMemoryStorage
        from spamfighter.core.storage.dbm import DomainedDBMStorage
        from spamfighter.core.log import MessageLog
        from spamfighter.core.counters import RequestPerSecondCounter, RequestCounter, AverageServiceTimeCounter
        domain = BaseDomain(parent=getDefaultDomain(), key='sample_root')
        rules = ('\ndo lengthCheck(minLength=1, maxLength=1000) mark invalid\ndo regexpCheck(regexp="[a-z]+") mark notalpha\nif invalid, notalpha skip to 1000\ndo messageFloodCheck() mark flood\ndo messageFrequencyCheck() mark messagefrequent, frequent\ndo userFrequencyCheck() mark userfrequent, frequent\nif frequent skip to 1000\ndo modelClassify(model="model2") mark spam\ndo messageLogPut(log="messageLog2")\n1000: do messageLogPut()\nif invalid stop as INVALID\nif frequent stop as FREQUENT\nif spam stop as SPAM\nstop as OK\n        ').strip()
        domain.set('model', BayesModel())
        domain.set('model2', BayesModel())
        domain.set('messageAnalyzer', MessageFirewall(rules))
        domain.set('storage', DomainMemoryStorage())
        domain.set('logStorage', DomainMemoryStorage())
        domain.set('db', DomainedDBMStorage())
        domain.set('messageLog', MessageLog(storage='logStorage'))
        domain.set('messageLog2', MessageLog(storage='logStorage'))
        domain.set('counterRequest', RequestCounter())
        domain.set('counterRPS', RequestPerSecondCounter())
        domain.set('counterAST', AverageServiceTimeCounter())

        def fillS1(subdomain_1):
            subdomain_1.set('model2', BayesModel())
            subdomain_1.set('counterRequest', RequestCounter())
            subdomain_1.set('counterRPS', RequestPerSecondCounter())
            subdomain_1.set('counterAST', AverageServiceTimeCounter())

            def fillS1_1(subdomain_1_1):
                subdomain_1_1.set('messageLog', MessageLog(storage='logStorage'))

            subdomain_1.createSubdomain('s1_1').addCallback(fillS1_1)

        domain.createSubdomain('s1').addCallback(fillS1)
        domain.createSubdomain('s2')
        return domain


sampleDomainProvider = SampleDomainProvider()