# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v2/test_python.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1106 bytes
import unittest
from bookshelf.api_v2 import python
from fabric.api import sudo, run
from bookshelf.tests.api_v2.docker_based_tests import with_ephemeral_container, prepare_required_docker_images

class UpdateSystemPipToLatestPipUbuntuTests(unittest.TestCase):

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh',
     'ubuntu-trusty-ruby-ssh'])
    def test_update_system_pip_to_latest_pip(self, *args, **kwargs):
        python.update_system_pip_to_latest_pip()
        self.assertRegexpMatches(sudo('pip --version'), 'pip 8.* from.*')


class UpdateToLatestPipUbuntuTests(unittest.TestCase):

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh',
     'ubuntu-trusty-ruby-ssh'])
    def test_update_to_latest_pip(self, *args, **kwargs):
        python.update_to_latest_pip()
        self.assertRegexpMatches(run('pip --version'), 'pip 8.* from.*')


if __name__ == '__main__':
    prepare_required_docker_images()
    unittest.main(verbosity=4, failfast=True)