# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0002_check_resources.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import settings
from pycore import Cloud
from pycore.utils import CloudException
api = None
cloud = None

def setup_module(module):
    global api
    global cloud
    cloud = Cloud(settings.address, settings.login, settings.password, debug=True)
    api = cloud.get_api()


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_check_compute_caps():
    available = False
    caps = api.template_capabilities()
    if len(caps.keys()) == 0:
        raise Exception('no defined hardware templates')
    for t in caps.keys():
        if caps[t] > 0:
            available = True

    if not available:
        raise Exception('no computing resources available')


def test_check_network_caps():
    isolated_available = False
    routed_available = False
    public_available = False
    for n in api.network_pool_list():
        if n.mode == 'isolated' and n.state == 'ok':
            isolated_available = True
        if n.mode == 'routed' and n.state == 'ok':
            routed_available = True
        if n.mode == 'public' and n.state == 'ok':
            public_available = True

    if not isolated_available:
        raise Exception('no isolated network pool available')
    if not routed_available:
        raise Exception('no routed network pool available')
    if not public_available:
        raise Exception('no public network pool available')


def test_check_storage_caps():
    available = False
    caps = api.storage_capabilities()
    if caps == 0:
        raise Exception('no storages defined or available')
    if caps < 10000:
        raise Exception('not enough storage space available')