# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/clssecurity.py
# Compiled at: 2010-12-12 22:28:56
import os, sys, gnupg
from conf import settings
import testcase_settings
from borg import Borg

class ClsSecurity(Borg):

    def __init__(self):
        print 'Class created: %s' % self.__class__.__name__
        Borg.__init__(self)
        self.gpg = gnupg.GPG(gnupghome=settings.PGPHOMEDIR)

    def __repr__(self):
        pass

    def setFingerprint(self, fingerprint):
        self.fingerprint = fingerprint

    def run(self):
        return self.__repr__()

    def decrypt(self, encPayload):
        uData = str(self.gpg.decrypt(encPayload, passphrase=settings.PASSPHRASE))
        return uData

    def decryptFile(self, filename):
        stream = open(filename, 'rb')
        if settings.PASSPHRASE == '':
            ascii_data = self.gpg.decrypt_file(stream, always_trust=True)
        else:
            ascii_data = self.gpg.decrypt_file(stream, passphrase=settings.PASSPHRASE)
        stream.close()
        return str(ascii_data)

    def decryptFile2Stream(self, filename):
        from StringIO import StringIO
        uData = self.decryptFile(filename)
        uDataStream = StringIO(uData)
        return uDataStream

    def listKeys(self):
        keys = self.gpg.list_keys()
        print keys

    def encrypt(self, payload):
        encrypted_ascii_data = self.gpg.encrypt(payload, self.fingerprint)
        return encrypted_ascii_data

    def encryptFile(self, filename, encryptedFile):
        stream = open(filename, 'r')
        encrypted_ascii_data = self.gpg.encrypt_file(stream, self.fingerprint)
        outFile = open(encryptedFile, 'w')
        outFile.write(str(encrypted_ascii_data))
        outFile.close()
        stream.close()


def main():
    cls = ClsSecurity()
    inputFile = os.path.join(testcase_settings.INPUTFILES_PATH, testcase_settings.XML_DECRYPTED_FILE)
    outputFile = inputFile + '.gpg'
    cls.setFingerprint('97A798CF9E8D9F470292975E70DE787C6B57800F')
    cls.encryptFile(inputFile, outputFile)
    dData = cls.decryptFile(outputFile)
    stream = open(inputFile, 'r')
    uData = stream.read()
    if uData == dData:
        print 'same'
    else:
        print 'different'
    cls.run()
    cls.listKeys()


if __name__ == '__main__':
    sys.exit(main())