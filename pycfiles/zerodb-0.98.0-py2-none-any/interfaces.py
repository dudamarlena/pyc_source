# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /zerodb/transform/interfaces.py
# Compiled at: 2015-12-09 01:37:29
from zope.interface import Attribute, Interface

class ICompressor(Interface):
    """Compressing or decompressing data"""
    name = Attribute("Signature that object is compressed with this algorithm. Recorded as '.cname$'")
    _compress = Attribute('Low-level compress function')
    _decompress = Attribute('Low-level decompress function')

    def compress(data):
        """Compresses data"""
        pass

    def decompress(data):
        """Decompresses data"""
        pass

    def register(default):
        """Register utility"""
        pass


class IEncrypterClass(Interface):
    """Class which marks encrypting interface, not encrypting object"""
    pass


class IEncrypter(Interface):
    """Encrypting or decrypting data"""
    name = Attribute("Signature that object is encrypted with this algorithm. Recorded as '.ename$'")
    attributes = Attribute('List of attributes to consume from init')

    def encrypt(data):
        """Encrypts data"""
        pass

    def decrypt(data):
        """Decrypts data"""
        pass

    def _encrypt(data):
        """Low level encrypt interface"""
        pass

    def _decrypt(data):
        """Low level decrypt interface"""
        pass

    def _init_encryption(**kw):
        """Extra functions to init encryption"""
        pass