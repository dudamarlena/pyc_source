# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/tests/api_v2/test_vagrant.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1110 bytes
import unittest
from bookshelf.api_v2 import vagrant
from fabric.api import run, sudo
from bookshelf.tests.api_v2.vagrant_based_tests import with_ephemeral_vagrant_box

class VagrantBasedTests(unittest.TestCase):

    @with_ephemeral_vagrant_box(verbose=True, images=[
     'ubuntu/trusty64', 'ubuntu/vivid64'])
    def test_vagrant_module(self, *args, **kwargs):
        vagrant.install_virtualbox(distribution='ubuntu', force_setup=True)
        self.assertTrue(sudo('dpkg-query -l virtualbox-5.0| grep -q ^.i').return_code == 0)
        vagrant.install_vagrant(distribution='ubuntu', version='1.7.4')
        run('vagrant init')
        self.assertTrue('Vagrantfile' in run('ls'))
        vagrant.install_vagrant_plugin(plugin='ansible')
        self.assertTrue('ansible' in run('vagrant plugin list'))
        self.assertTrue(vagrant.is_vagrant_plugin_installed('ansible'))


if __name__ == '__main__':
    unittest.main(verbosity=4, failfast=True)