# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v2/test_java.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1275 bytes
import unittest
from bookshelf.api_v2 import java
from fabric.api import sudo, run
from bookshelf.tests.api_v2.docker_based_tests import with_ephemeral_container, prepare_required_docker_images

class InstallOracleJavaTests(unittest.TestCase):

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh', 'ubuntu-trusty-ruby-ssh'])
    def test_install_oracle_java_installs_java_on_ubuntu(self, *args, **kwargs):
        java.install_oracle_java(distribution='ubuntu', java_version='8')
        self.assertRegexpMatches(run('java -version '), '.*java version "1.8.*".*')

    @with_ephemeral_container(images=[
     'ubuntu-vivid-ruby-ssh', 'ubuntu-trusty-ruby-ssh'])
    def test_install_oracle_java_raises_exception_on_failure(self, *args, **kwargs):
        sudo('echo > /etc/resolv.conf')
        with self.assertRaises(SystemExit) as (cm):
            java.install_oracle_java(distribution='ubuntu', java_version='8')
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    prepare_required_docker_images()
    unittest.main(verbosity=4, failfast=True)