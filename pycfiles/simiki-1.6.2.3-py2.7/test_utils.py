# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/tests/test_utils.py
# Compiled at: 2017-02-26 00:05:19
from __future__ import print_function, unicode_literals
import os, os.path, unittest
from simiki import utils
test_path = os.path.dirname(os.path.abspath(__file__))

class TestUtils(unittest.TestCase):

    def setUp(self):
        wiki_path = os.path.join(test_path, b'mywiki_for_others')
        os.chdir(wiki_path)
        self.content = b'content'
        self.output = b'output'
        if os.path.exists(self.output):
            utils.emptytree(self.output)
            os.rmdir(self.output)

    def test_check_extension(self):
        valid_files = [b'/tmp/file1.md', b'/tmp/file2.mkd', b'/tmp/文件3.mdown',
         b'/tmp/文件4.markdown', b'/tmp/目录/文件5.md']
        for f in valid_files:
            assert utils.check_extension(f)

        invalid_files = [b'/tmp/file6.txt', b'/tmp/目录/文件7.mkdown']
        for f in invalid_files:
            assert not utils.check_extension(f)

    def test_copytree_common(self):
        utils.copytree(self.content, self.output)
        assert os.path.exists(self.output) and os.path.isdir(self.output)
        files = [
         os.path.join(b'python', b'zen_of_python.md'),
         os.path.join(b'python', b'python文档.md'),
         os.path.join(b'其它', b'helloworld.markdown'),
         os.path.join(b'其它', b'维基.md'),
         os.path.join(b'其它', b'hello.txt'),
         os.path.join(b'其它', b'.hidden.md')]
        for f in files:
            assert os.path.exists(os.path.join(self.output, f))

    def test_copytree_symlink(self):
        """temp not support"""
        pass

    def test_copytree_ignore(self):
        """temp not support"""
        pass

    def test_emptytree(self):
        utils.copytree(self.content, self.output)
        utils.emptytree(self.output)
        assert not os.listdir(self.output)

    def test_mkdir_p(self):
        path = os.path.join(self.content)
        utils.mkdir_p(path)
        assert os.path.exists(path)
        path = os.path.join(self.output, b'dir1/dir2/dir3')
        utils.mkdir_p(path)
        assert os.path.exists(path)
        path = os.path.join(self.content, b'其它', b'hello.txt')
        self.assertRaises(OSError, lambda : utils.mkdir_p(path))

    def test_listdir_nohidden(self):
        fs = utils.listdir_nohidden(os.path.join(self.content, b'其它'))
        expected_listdir = [b'hello.txt', b'helloworld.markdown', b'维基.md']
        assert sorted(list(fs)) == sorted(expected_listdir)

    def test_get_md5(self):
        test_file = os.path.join(self.content, b'python', b'zen_of_python.md')
        self.assertEqual(b'd6e211679cb75b24c4e62fb233483fea', utils.get_md5(test_file))

    def test_get_dir_md5(self):
        test_dir = os.path.join(self.content, b'python')
        self.assertEqual(b'ab2bf30fc9b8ead85e52fd19d02a819e', utils.get_dir_md5(test_dir))

    def tearDown(self):
        if os.path.exists(self.output):
            utils.emptytree(self.output)
            os.rmdir(self.output)


if __name__ == b'__main__':
    unittest.main()