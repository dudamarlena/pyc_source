# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DPAPI/Probes/skype.py
# Compiled at: 2014-09-22 08:18:41
from xml import etree
import hashlib, struct, array, M2Crypto
from DPAPI import probe
from DPAPI.Core import blob

class SkypeAccount(probe.DPAPIProbe):

    def parse(self, data):
        self.login = None
        self.cleartext = None
        self.dpapiblob = blob.DPAPIBlob(data.remain())
        self.entropy = None
        return

    def preprocess(self, **k):
        self.login = k.get('login')
        tree = etree.ElementTree()
        if k.get('xmlfile') is not None:
            tree.parse(k['xmlfile'])
        else:
            tree.fromstring(k['xml'])
        self.cred = tree.find('.//Account/Credentials2')
        if self.cred is None:
            self.cred = tree.find('.//Account/Credentials3')
        if self.cred is not None:
            self.cred = self.cred.text.decode('hex')
        return

    def postprocess(self, **k):
        if self.cred is None:
            return
        else:
            k = hashlib.sha1(struct.pack('>L', 0) + self.dpapiblob.cleartext).digest()
            k += hashlib.sha1(struct.pack('>L', 1) + self.dpapiblob.cleartext).digest()
            ciph = M2Crypto.EVP.Cipher('aes_256_ecb', k[:32], '', M2Crypto.encrypt, 0)
            arr = array.array('B')
            arr.fromstring(self.cred)
            for i in range(0, len(self.cred), 16):
                buff = ciph.update('\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' + struct.pack('>L', i >> 4))
                for j in range(min(16, len(self.cred) - i)):
                    arr[(i + j)] ^= ord(buff[j])

            self.cleartext = arr.tostring().encode('hex')
            return

    def __getattr__(self, name):
        return getattr(self.dpapiblob, name)

    def jtr_shadow(self):
        if self.login is not None:
            return '%s:$dynamic_1401$%s' % (self.login, self.cleartext[:32])
        else:
            return ''

    def __repr__(self):
        s = ['Skype account']
        if self.login is not None:
            s.append('        login = %s' % self.login)
        s.append('        hash  = %s' % self.cleartext[:32])
        return ('\n').join(s)