# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeremydw/git/pygrow/env/lib/python2.7/site-packages/jetway/jetway_test.py
# Compiled at: 2015-01-24 14:48:40
import os, unittest, jetway
TEST_BUILD_DIR = os.path.join(os.path.dirname(__file__), 'testdata', 'build')

class JetwayTestCase(unittest.TestCase):

    def test_exception(self):

        def raise_error():
            raise jetway.GoogleStorageRpcError(403, 'Forbidden.')

        self.assertRaises(jetway.GoogleStorageRpcError, raise_error)

    def test_client(self):
        self.assertRaises(ValueError, jetway.Jetway, 'foo', 'bar', 'baz')
        client = jetway.Jetway(project='jeremydw/test', name='test-staging-site', host='grow-prod.appspot.com', secure=True)
        client.login()
        paths_written, errors = client.upload_dir(TEST_BUILD_DIR)
        for basename in os.listdir(TEST_BUILD_DIR):
            self.assertIn(('/{}').format(basename), paths_written)

        self.assertEqual({}, errors)
        paths_to_contents = {'/foo.html': 'hello foo', 
           '/bar.html': 'hello bar'}
        paths_written, errors = client.write(paths_to_contents)
        for path in paths_to_contents.keys():
            self.assertIn(path, paths_written)

        self.assertEqual({}, errors)
        paths_read, errors = client.read(paths_to_contents.keys())
        for path, content in paths_read.iteritems():
            self.assertEqual(paths_to_contents[path], content)

        self.assertEqual({}, errors)
        deleted_path = paths_to_contents.keys()[1]
        paths_deleted, errors = client.delete([deleted_path])
        self.assertIn(deleted_path, paths_deleted)
        self.assertEqual({}, errors)
        paths_read, errors = client.read([deleted_path])
        self.assertEqual({}, paths_read)
        self.assertTrue(isinstance(errors[deleted_path], jetway.GoogleStorageRpcError))


if __name__ == '__main__':
    unittest.main()