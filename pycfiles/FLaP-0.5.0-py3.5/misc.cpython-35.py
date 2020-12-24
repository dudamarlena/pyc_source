# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\acceptance\misc.py
# Compiled at: 2016-12-19 09:08:19
# Size of source mod 2**32: 2073 bytes
from unittest import TestCase, main as testmain
from flap.util.oofs import OSFileSystem
from flap.util.path import TEMP

class OSFileSystemTest(TestCase):

    def setUp(self):
        self.fileSystem = OSFileSystem()
        self.path = TEMP / 'flap_os' / 'test.txt'
        self.content = 'blahblah blah'
        self.fileSystem.deleteDirectory(TEMP / 'flap_os')
        self.fileSystem.deleteDirectory(TEMP / 'flatexer_copy')

    def createAndOpenTestFile(self):
        self.fileSystem.create_file(self.path, self.content)
        return self.fileSystem.open(self.path)

    def testCreateAndOpenFile(self):
        file = self.createAndOpenTestFile()
        self.assertEqual(file.content(), self.content)

    def testCopyAndOpenFile(self):
        file = self.createAndOpenTestFile()
        copyPath = TEMP / 'flatexer_copy'
        self.fileSystem.copy(file, copyPath)
        copy = self.fileSystem.open(copyPath / 'test.txt')
        self.assertEqual(copy.content(), self.content)

    def test_copyAndRename(self):
        file = self.createAndOpenTestFile()
        copy_path = TEMP / 'dir' / 'copy.txt'
        self.fileSystem.copy(file, copy_path)
        copy = self.fileSystem.open(copy_path)
        self.assertEqual(copy.content(), self.content)


if __name__ == '__main__':
    testmain()