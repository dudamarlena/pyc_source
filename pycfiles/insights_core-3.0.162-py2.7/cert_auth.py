# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/client/cert_auth.py
# Compiled at: 2019-05-16 13:41:33
"""
Module to interact with Satellite Based Certificates
"""
from __future__ import print_function
import os, logging
logger = logging.getLogger(__name__)
RHSM_CONFIG = None
try:
    from rhsm.config import initConfig
    from rhsm.certificate import create_from_pem
    RHSM_CONFIG = initConfig()
except ImportError:
    logger.debug('Could not load RHSM modules')

class rhsmCertificate:
    try:
        PATH = RHSM_CONFIG.get('rhsm', 'consumerCertDir')
    except:
        pass

    KEY = 'key.pem'
    CERT = 'cert.pem'

    @classmethod
    def keypath(cls):
        return os.path.join(cls.PATH, cls.KEY)

    @classmethod
    def certpath(cls):
        return os.path.join(cls.PATH, cls.CERT)

    @classmethod
    def read(cls):
        f = open(cls.keypath())
        key = f.read()
        f.close()
        f = open(cls.certpath())
        cert = f.read()
        f.close()
        return rhsmCertificate(key, cert)

    @classmethod
    def exists(cls):
        return os.path.exists(cls.keypath()) and os.path.exists(cls.certpath())

    @classmethod
    def existsAndValid(cls):
        if cls.exists():
            try:
                cls.read()
                return True
            except Exception as e:
                print(e)

        return False

    def __init__(self, keystring, certstring):
        self.key = keystring
        self.cert = certstring
        self.x509 = create_from_pem(certstring)

    def getConsumerId(self):
        subject = self.x509.subject
        return subject.get('CN')

    def getConsumerName(self):
        altName = self.x509.alt_name
        return altName.replace('DirName:/CN=', '')

    def getSerialNumber(self):
        return self.x509.serial

    def __str__(self):
        return 'consumer: name="%s", uuid%s' % (
         self.getConsumerName(),
         self.getConsumerId())