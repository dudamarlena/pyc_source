# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v2/test_file.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 3577 bytes
import unittest
from bookshelf.api_v2 import file
from fabric.api import sudo, run
from bookshelf.tests.api_v2.docker_based_tests import with_ephemeral_container, prepare_required_docker_images

class InsertLineInFileAfterRegexTests(unittest.TestCase):

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh',
     'ubuntu-trusty-ruby-ssh',
     'centos-7-ruby-ssh'])
    def test_insert_line_in_file_after_regex_returns_True_when_changed(self, *args, **kwargs):
        contents = '\n'.join([
         'Here I am,',
         'on my bicycle',
         'cool, init?'])
        run('echo "%s" > /tmp/test' % contents)
        self.assertTrue(file.insert_line_in_file_after_regex('/tmp/test', 'Look mum, no hands', '.*on.*bicycle'))

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh',
     'ubuntu-trusty-ruby-ssh',
     'centos-7-ruby-ssh'])
    def test_insert_line_in_file_after_regex_returns_False_when_not_changed(self, *args, **kwargs):
        contents = '\n'.join([
         'Here I am,',
         'on my bicycle',
         'Look mum, no hands',
         'cool, init?'])
        run('echo "%s" > /tmp/test' % contents)
        self.assertFalse(file.insert_line_in_file_after_regex('/tmp/test', 'Look mum, no hands', '.*on.*bicycle'))

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh',
     'ubuntu-trusty-ruby-ssh',
     'centos-7-ruby-ssh'])
    def test_insert_line_in_file_after_regex_inserts_line(self, *args, **kwargs):
        contents = '\n'.join([
         'Here I am,',
         'on my bicycle',
         'cool, init?'])
        expected = '\r\n'.join([
         'Here I am,',
         'on my bicycle',
         'Look mum, no hands',
         'cool, init?'])
        run('echo "%s" > /tmp/test' % contents)
        file.insert_line_in_file_after_regex('/tmp/test', 'Look mum, no hands', '.*on.*bicycle')
        self.assertEqual(sudo('cat /tmp/test'), expected)

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh',
     'ubuntu-trusty-ruby-ssh',
     'centos-7-ruby-ssh'])
    def test_insert_line_in_file_after_regex_raises_Exception_on_failure(self, *args, **kwargs):
        with self.assertRaises(SystemExit) as (cm):
            file.insert_line_in_file_after_regex('/tmp/test', 'Look mum, no hands', '.*on.*bicycle')
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    prepare_required_docker_images()
    unittest.main(verbosity=4, failfast=True)