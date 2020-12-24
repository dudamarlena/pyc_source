# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/mail/vocabulary.py
# Compiled at: 2012-04-02 04:44:23
from zope.schema.interfaces import IVocabularyFactory
from zope.sendmail.interfaces import IMailDelivery
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import classProvides

class MailDeliveryVocabulary(UtilityVocabulary):
    """Mail delivery utilities"""
    classProvides(IVocabularyFactory)
    interface = IMailDelivery
    nameOnly = True