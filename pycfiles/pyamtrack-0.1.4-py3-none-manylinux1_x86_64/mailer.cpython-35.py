# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_mail/mailer.py
# Compiled at: 2020-02-20 09:58:33
# Size of source mod 2**32: 1020 bytes
__doc__ = 'PyAMS_mailer.mailer module\n\nThis module provides a vocabulary of registered mailers utilities.\n'
from pyramid_mailer.interfaces import IMailer
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from pyams_mail.interfaces import MAILERS_VOCABULARY_NAME
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@vocabulary_config(name=MAILERS_VOCABULARY_NAME)
class MailerVocabulary(UtilityVocabulary):
    """MailerVocabulary"""
    interface = IMailer
    nameOnly = True