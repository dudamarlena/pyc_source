# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/plonecrypto/interfaces.py
# Compiled at: 2010-04-12 02:19:54
"""
define the interfaces for leocornus.plonecrypto.
"""
from zope.interface import Interface
from zope.interface import Attribute
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class IPloneCryptoTool(Interface):
    """
    providing easy way for cryptography in Plone
    """
    __module__ = __name__
    id = Attribute('id', 'Must set to "leocornus_crypto"')


class IPloneCrypter(Interface):
    """
    providing the APIs for doing cryptography in a Plone site.
    """
    __module__ = __name__

    def encrypt(message):
        """
        Return an encrypted message for the given raw message.
        """
        pass

    def decrypt(message):
        """
        Return the raw message for the given encrypted message.
        """
        pass