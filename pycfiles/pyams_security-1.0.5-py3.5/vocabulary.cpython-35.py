# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/vocabulary.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 1020 bytes
"""PyAMS_security.vocabulary module

"""
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.password.interfaces import IPasswordManager
from pyams_security.interfaces import PASSWORD_MANAGERS_VOCABULARY_NAME
from pyams_utils.vocabulary import vocabulary_config
__docformat__ = 'restructuredtext'

@vocabulary_config(name=PASSWORD_MANAGERS_VOCABULARY_NAME)
class PasswordManagerVocabulary(UtilityVocabulary):
    __doc__ = 'Password managers vocabulary'
    interface = IPasswordManager
    nameOnly = True