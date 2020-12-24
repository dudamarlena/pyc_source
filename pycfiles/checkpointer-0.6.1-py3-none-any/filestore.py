# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/tests/filestore.py
# Compiled at: 2009-01-06 11:27:52
__doc__ = 'Unit-test the Checkpoint FileStore'
import os, shutil, errno, hashlib, tempfile, unittest
from checkpoint.error import *
from checkpoint.util import descending_length
from checkpoint.filestore import FileStore, FILE, DIRECTORY, LINK
__all__ = [
 'TempFileTestCase', 'FileStoreTest']

class TempFileTestCase(unittest.TestCase):
    test_files = [
     'a.txt',
     'b.txt',
     'c.txt',
     'alink->a.txt',
     'morestuff/',
     'morestuff/d.txt',
     'morestuff/evenmore/',
     'morestuff/evenmore/e.txt']

    def format_path(self, unixpath):
        """Format a temp file path in the os-specific format."""
        return os.path.join(self.temp_dir, unixpath.replace('/', os.sep))

    def create_temp_files(self, paths):
        """Create the specified files and directories in the temp dir."""
        for path in paths:
            if '->' in path:
                (link, target) = path.split('->')
                link = self.format_path(link)
                target = self.format_path(target)
                os.symlink(target, link)
            else:
                fullpath = self.format_path(path)
                if path.endswith('/'):
                    os.mkdir(fullpath)
                else:
                    f = open(fullpath, 'w')
                    f.write('TEST DATA!')
                    f.close()

    def setUp(self):
        """Prepare test environment (basic setup shared between all tests)."""
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'filestoretests')
        try:
            shutil.rmtree(self.temp_dir)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise

        os.mkdir(self.temp_dir)
        os.chdir(self.temp_dir)

    def tearDown(self):
        """Remove resources used by test environment."""
        os.chdir(self.temp_dir)
        os.chdir(os.pardir)
        shutil.rmtree(self.temp_dir)


class FileStoreTest(TempFileTestCase):

    def setUp(self):
        TempFileTestCase.setUp(self)
        self.repository = os.path.join(self.temp_dir, '.cpt')
        os.mkdir(self.repository)
        self.create_temp_files(self.test_files)
        self.filestore = FileStore(self.repository)

    def testKnownFileTypes(self):
        """get_file_type should work for supported file types."""
        for path in self.test_files:
            fullpath = self.format_path(path.split('->')[0])
            file_type = self.filestore.get_file_type(fullpath)
            if '->' in path:
                self.assertEqual(file_type, LINK)
            elif path.endswith('/'):
                self.assertEqual(file_type, DIRECTORY)
            else:
                self.assertEqual(file_type, FILE)

    def testUnknownFileTypes(self):
        """Sockets and non-existant files should raise an error."""
        socketpath = self.format_path('mysocket')
        os.mkfifo(socketpath)
        self.assertRaises(UnsupportedFileType, self.filestore.get_file_type, socketpath)
        notafile = self.format_path('SomePathThatsNotAFile')
        self.assertRaises(NotFound, self.filestore.get_file_type, notafile)

    def testRepositoryNotInitialized(self):
        """Uninitialized FileStores should raise an error on save()."""
        path = self.test_files[0]
        fullpath = self.format_path(path.split('->')[0])
        some_hash = '000111'
        file_type = self.filestore.get_file_type(fullpath)
        self.assertRaises(UninitializedRepositoryError, self.filestore.save, fullpath, some_hash, some_hash, file_type)

    def testStoreFiles(self):
        """save should not raise an error."""
        self.filestore.initialize()
        for path in self.test_files:
            fullpath = self.format_path(path.split('->')[0])
            some_hash = hashlib.sha1(fullpath).hexdigest()
            file_type = self.filestore.get_file_type(fullpath)
            self.filestore.save(fullpath, some_hash, some_hash, file_type)

    def testDeleteFiles(self):
        """delete should actually delete files."""
        path_infos = []
        deepest_first = self.test_files[:]
        deepest_first.sort(cmp=descending_length)
        for path in deepest_first:
            fullpath = self.format_path(path.split('->')[0])
            some_hash = hashlib.sha1(fullpath).hexdigest()
            file_type = self.filestore.get_file_type(fullpath)
            path_infos.append((
             fullpath, some_hash, some_hash, file_type))
            self.filestore.delete(fullpath)
            self.assertFalse(os.path.exists(fullpath))

        return path_infos

    def testRestoreFiles(self):
        """restore_multiple should correctly restore deleted files."""
        self.testStoreFiles()
        path_infos = self.testDeleteFiles()
        self.filestore.restore_multiple(path_infos)
        for path in self.test_files:
            fullpath = self.format_path(path.split('->')[0])
            self.assertTrue(os.path.exists(fullpath))


if __name__ == '__main__':
    unittest.main()