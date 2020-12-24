# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/security_unit_test.py
# Compiled at: 2010-12-12 18:24:12
"""Unit-tests various encryption/decryption scenarios (called tests also) in 
clssecurity.py."""
from clssecurity import ClsSecurity
import unittest, os, testcase_settings, postgresutils

class CryptTestCase(unittest.TestCase):
    """see if the return value is a file path"""

    def test_decrypt_valid(self):
        """Tests to see if we can decrypt a known file and compare that with existing 'unencrypted' version of the file"""
        security = ClsSecurity()
        instance_filename = os.path.join('%s' % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_ENCRYPTED_FILE)
        sourceFile = os.path.join('%s' % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        dData = security.decryptFile(instance_filename)
        stream = open(sourceFile, 'r')
        uData = stream.read()
        self.assertEqual(uData, dData)
        stream.close()

    def test_encrypt_valid(self):
        """Tests we can encrypt a file.  Encrypted file will be compared against a known "encrypted" file outside of framework"""
        security = ClsSecurity()
        instance_filename = os.path.join('%s' % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_DECRYPTED_FILE)
        outputFile = instance_filename + '.asc'
        inputFile = os.path.join('%s' % testcase_settings.INPUTFILES_PATH, testcase_settings.XML_FILE_VALID)
        security.setFingerprint(testcase_settings.XML_ENCRYPT_FINGERPRINT)
        security.encryptFile(instance_filename, outputFile)
        dData = security.decryptFile(outputFile)
        stream = open(inputFile, 'r')
        uData = stream.read()
        self.assertEqual(uData, dData)
        stream.close()


if __name__ == '__main__':
    unittest.main()