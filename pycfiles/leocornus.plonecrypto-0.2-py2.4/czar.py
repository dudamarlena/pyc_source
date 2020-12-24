# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/plonecrypto/crypter/czar.py
# Compiled at: 2010-04-16 03:23:27
"""
keyczar implementation for Plone Crypter.
"""
import time
from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations
from keyczar import keyinfo
from keyczar.keydata import KeyMetadata
from keyczar.readers import Reader
from keyczar.keyczar import GenericKeyczar
from keyczar.keyczar import Crypter
from keyczar.errors import KeyczarError
from base import BaseCrypter
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'
KEYCZAR_ANNO_META = 'leocornus.plonecrypto.crypter.keyczar.meta'
KEYCZAR_ANNO_KEYS = 'leocornus.plonecrypto.crypter.keyczar.keys'
LOGGING_KEY = 'leocornus.plonecrypto.crypter.keyczar.logging'

class PloneKeyczarCrypter(BaseCrypter):
    """
    depends on keyczar-python to imeplement Plone Crypter.
    """
    __module__ = __name__

    def __init__(self, context):
        self.context = context
        self.enableLog = aq_inner(self.context).enableLog
        self.anno = IAnnotations(self.context)
        if not self.anno.has_key(LOGGING_KEY):
            self.anno[LOGGING_KEY] = []
        if not self.anno.has_key(KEYCZAR_ANNO_KEYS):
            self.anno[KEYCZAR_ANNO_KEYS] = {}
        if not self.anno.has_key(KEYCZAR_ANNO_META):
            self.createKeyset()
            self.addPrimaryKey()

    def log(self, message):
        """
        logging the keys management.
        """
        if not self.enableLog:
            return
        fmtMessage = '%s - %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), message)
        self.anno[LOGGING_KEY].insert(0, fmtMessage)

    def clearLogs(self):
        self.anno[LOGGING_KEY] = []

    def getLogs(self):
        """
        return all logs if have.
        """
        return self.anno[LOGGING_KEY]

    def keysAmount(self):
        """
        return the total amount of keys.
        """
        return len(self.anno[KEYCZAR_ANNO_KEYS])

    def writeAnnotations(self, keyczar):
        self.anno[KEYCZAR_ANNO_META] = str(keyczar.metadata)
        for v in keyczar.versions:
            self.anno[KEYCZAR_ANNO_KEYS][v.version_number] = str(keyczar.GetKey(v))

    def createKeyset(self, asymmetric=keyinfo.RSA_PRIV):
        """
        create a new keyset and save to the annotation
        """
        name = 'PloneCrypter'
        purpose = keyinfo.DECRYPT_AND_ENCRYPT
        kmd = KeyMetadata(name, purpose, asymmetric)
        self.anno[KEYCZAR_ANNO_META] = str(kmd)

    def addPrimaryKey(self):
        """
        add a new key as primary key.
        """
        keyczar = GenericKeyczar(AnnotationReader(self.context))
        status = keyinfo.PRIMARY
        size = None
        keyczar.AddVersion(status, size)
        self.writeAnnotations(keyczar)
        self.log('Added a new key as primary key; we have %s keys in total!' % len(keyczar.versions))
        return

    def removeOldestKey(self):
        """
        remove the oldest key from the chain.
        """
        versions = self.anno[KEYCZAR_ANNO_KEYS].keys()
        versions.sort()
        oldest_version = versions[0]
        keyczar = GenericKeyczar(AnnotationReader(self.context))
        keyczar.Demote(oldest_version)
        keyczar.Revoke(oldest_version)
        self.writeAnnotations(keyczar)
        self.anno[KEYCZAR_ANNO_KEYS].pop(oldest_version)
        self.log('Removed the oldest key: %s; we have %s keys in total!' % (oldest_version, len(keyczar.versions) - 1))

    def clearKeys(self):
        """
        remove the key metadata and destroy all keys.
        """
        keyczar = GenericKeyczar(AnnotationReader(self.context))
        for v in keyczar.versions:
            self.anno[KEYCZAR_ANNO_KEYS].pop(v.version_number)

        self.anno.pop(KEYCZAR_ANNO_META)
        self.log('Retired / Removed all %s keys!' % len(keyczar.versions))
        self.createKeyset()
        self.addPrimaryKey()

    def encrypt(self, message):
        crypter = Crypter(AnnotationReader(self.context))
        return crypter.Encrypt(message)

    def decrypt(self, message):
        crypter = Crypter(AnnotationReader(self.context))
        return crypter.Decrypt(message)


class AnnotationReader(Reader):
    """
    using annotations to store the metadata and keys.
    """
    __module__ = __name__

    def __init__(self, context):
        self.context = context
        self.anno = IAnnotations(self.context)

    def GetMetadata(self):
        return self.anno[KEYCZAR_ANNO_META]

    def GetKey(self, version_number):
        return self.anno[KEYCZAR_ANNO_KEYS][version_number]


class FileKeyczarCrypter(BaseCrypter):
    """
    A Keyczar crypter implementation based on default File reader.
    """
    __module__ = __name__

    def __init__(self, context):
        self.context = context
        self.crypter = Crypter.Read('/usr/local/rd/keyczar/rsa-keys')

    def encrypt(self, message):
        return self.crypter.Encrypt(message)

    def decrypt(self, message):
        return self.crypter.Decrypt(message)