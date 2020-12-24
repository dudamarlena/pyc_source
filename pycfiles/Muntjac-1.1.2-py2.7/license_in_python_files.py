# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/license_in_python_files.py
# Compiled at: 2013-04-04 15:36:37
from os import listdir
from os.path import exists, isdir, join, dirname
from unittest import TestCase
import muntjac

class LicenseInPythonFiles(TestCase):
    SRC_DIR = dirname(muntjac.__file__)

    def testPythonFilesContainsLicense(self):
        srcDir = self.SRC_DIR
        missing = set()
        self.checkForLicense(srcDir, missing)
        self.assertEquals(len(missing), 0, 'The following files are missing license information:\n' + ('\n').join(missing))

    def checkForLicense(self, srcDir, missing):
        self.assertTrue('Source directory ' + srcDir + ' does not exist', exists(srcDir))
        for f in listdir(srcDir):
            if isdir(f):
                self.checkForLicense(join(srcDir, f), missing)
            elif f.endswith('.py'):
                self.checkForLicenseInFile(join(srcDir, f), missing)

    def checkForLicenseInFile(self, f, missing):
        fd = None
        try:
            fd = open(f, 'rb')
            contents = fd.read()
            if 'Apache License, Version 2.0' not in contents:
                missing.add(f)
        finally:
            if fd is not None:
                fd.close()

        return