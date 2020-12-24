# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0000_install_node.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n              2016 Marta Nabozny\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import subprocess

def setup_module(module):
    pass


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_add_apt_repo():
    f = open('/etc/apt/sources.list.d/cloudover', 'w')
    f.write('deb http://packages.cloudover.org/nightly/ nightly main\n')
    f.close()


def test_update():
    subprocess.call(['apt-get', 'update'])


def test_upgrade():
    subprocess.call(['apt-get', 'upgrade', '--yes', '--force-yes'])


def test_install_packages():
    subprocess.call(['apt-get', 'install', '--yes', '--force-yes',
     'corenode',
     'ipython',
     'tcpdump'])