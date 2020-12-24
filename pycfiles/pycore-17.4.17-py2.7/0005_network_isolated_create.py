# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0005_network_isolated_create.py
# Compiled at: 2016-06-16 16:03:55
"""
Copyright (c) 2014 Maciej Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
    global network
    network = api.network_create(24, 'Normal Network', False, mode='isolated', address='10.0.0.0')


def test_lease_create():
    net_addr = IPNetwork(network.address + '/' + str(network.mask))
    for host in net_addr.iter_hosts():
        network.lease_create(host)


def test_list_leases():
    network.lease_list()


def test_network_release():
    network.release()


def test_create_test_network():
    networks = api.network_list()
    names = [ network.name for network in networks ]
    if 'Test isolated network' not in names:
        api.network_create(24, 'Test isolated network', False, address='10.0.0.0', mode='isolated')