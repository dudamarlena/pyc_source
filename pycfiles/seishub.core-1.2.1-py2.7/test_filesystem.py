# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\tests\test_filesystem.py
# Compiled at: 2011-01-03 17:15:11
"""
A test suite for file system resources.
"""
from seishub.core.exceptions import SeisHubError
from seishub.core.processor import GET, PUT, DELETE, POST, MOVE, Processor
from seishub.core.processor.resources.filesystem import FileSystemResource
from seishub.core.test import SeisHubEnvironmentTestCase
from twisted.web import http
import os, unittest
SPECIAL = [
 'Test !file',
 "Test '-'#$",
 'Test LongFilenamesWithMoreThan32Chars',
 'Test è or å,ä,ö',
 'Test üöäß']

class FileSystemTests(SeisHubEnvironmentTestCase):
    """
    A test suite for file system resources.
    """

    def setUp(self):
        path = os.path.dirname(__file__)
        fs_path = os.path.join(path, 'data', 'filesystem')
        self.env.tree = FileSystemResource(fs_path)

    def tearDown(self):
        pass

    def test_readFileSystemResourceWithSpecialChars(self):
        """
        Test to access folders and files with special chars.
        """
        proc = Processor(self.env)
        root = proc.run(GET, '/special')
        for dir in SPECIAL:
            self.assertTrue(dir in root)
            sub = proc.run(GET, '/special/' + dir)
            self.assertTrue('üöä.txt' in sub)
            fsobj = proc.run(GET, '/special/' + dir + '/üöä.txt')
            self.assertTrue(isinstance(fsobj, FileSystemResource))
            fh = fsobj.open()
            data = fh.read()
            fh.close()
            self.assertEquals(data, 'MÜH')

    def test_executeResourceScript(self):
        """
        Files with extension '.rpy' should be interpreted as Resource scripts.
        """
        proc = Processor(self.env)
        for method in [POST, PUT, DELETE, MOVE, GET]:
            data = proc.run(method, '/scripts/test.rpy')
            self.assertEquals('<html>%s</html>' % method, data)

    def test_notImplementedMethods(self):
        """
        Not implemented methods should raise an error.
        """
        proc = Processor(self.env)
        for method in ['MUH', 'XXX', 'GETPUT']:
            try:
                proc.run(method, '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/scripts/test.rpy')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

    def test_notAllowedMethods(self):
        """
        Not allowed methods should raise an error.
        """
        proc = Processor(self.env)
        for method in [POST, PUT, DELETE, MOVE]:
            try:
                proc.run(method, '')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)

            try:
                proc.run(method, '/')
                self.fail('Expected SeisHubError')
            except SeisHubError as e:
                self.assertEqual(e.code, http.NOT_ALLOWED)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FileSystemTests, 'test'))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')