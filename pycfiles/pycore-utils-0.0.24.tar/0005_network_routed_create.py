# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0005_network_routed_create.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import settings
from pycore import Cloud
from netaddr import IPAddress, IPNetwork
api = None
cloud = None
network_private = None
network_public = None
leases = None

def setup_module(module):
    global api
    global cloud
    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_network_create():
    global network_private
    global network_public
    network_public = api.network_create(24, 'Normal Network', False, mode='routed')
    network_private = api.network_create(24, 'Isolated Network', True, mode='routed')


def test_lease_create():
    net_addr = IPNetwork(network_public.address)
    for host in net_addr.iter_hosts():
        if IPNetwork('%s/30' % str(host + 2)) == host:
            network_public.lease_create(host)

    net_addr = IPNetwork(network_private.address)
    for host in net_addr.iter_hosts():
        if IPNetwork('%s/30' % str(host + 2)) == host:
            network_private.lease_create(host)


def test_list_leases():
    network_private.lease_list()


def test_network_release():
    network_private.release()
    network_public.release()


def test_create_test_network():
    networks = api.network_list()
    names = [ network.name for network in networks ]
    if 'Test routed network' not in names:
        api.network_create(24, 'Test routed network', False, mode='isolated')