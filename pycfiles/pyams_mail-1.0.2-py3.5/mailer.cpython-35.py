# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_mail/mailer.py
# Compiled at: 2020-02-20 09:58:33
# Size of source mod 2**32: 1020 bytes
"""PyAMS_mailer.mailer module

This module provides a vocabulary of registered mailers utilities.
"""
from pyramid_mailer.interfaces import IMailer
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from pyams_mail.interfaces import MAILERS_VOCABULARY_NAME
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@vocabulary_config(name=MAILERS_VOCABULARY_NAME)
class MailerVocabulary(UtilityVocabulary):
    __doc__ = 'Mailer vocabulary'
    interface = IMailer
    nameOnly = True