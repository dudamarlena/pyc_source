# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0005_network_redirection_lease.py
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
import time, settings
from pycore import Cloud
from netaddr import IPAddress, IPNetwork
api = None
cloud = None
network_private = None
network_public = None
public_lease = None
private_lease = None

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
    network_public = api.network_create(30, 'Public network', isolated=False, mode='public')
    network_private = api.network_create(24, 'Routed network', isolated=False, mode='routed')


def test_lease_create():
    net_addr = IPNetwork(network_public.address + '/' + str(network_public.mask))
    for host in net_addr.iter_hosts():
        network_public.lease_create(host)

    net_addr = IPNetwork(network_private.address + '/' + str(network_private.mask))
    for host in net_addr.iter_hosts():
        if IPNetwork('%s/30' % str(host)).network == host:
            network_private.lease_create(host + 2)


def test_list_leases():
    assert len(network_private.lease_list()) == 63
    assert len(network_public.lease_list()) == 2


def test_redirect_one():
    global private_lease
    global public_lease
    private_lease = network_private.lease_list()[0]
    public_lease = network_public.lease_list()[0]
    public_lease.redirect(private_lease)
    public_lease.remove_redirection(private_lease)


def test_wait_redirected():
    assert private_lease is not None
    assert public_lease is not None
    for i in xrange(120):
        lease = api.lease_by_id(private_lease.id)
        if lease.redirected_to is not None:
            return
        time.sleep(1)

    raise Exception('lease not redirected')
    return


def test_redirect_all():
    public_lease = network_public.lease_list()[0]
    for lease in network_private.lease_list():
        public_lease.redirect(lease)

    for lease in network_private.lease_list():
        public_lease.remove_redirection(lease)


def test_network_release():
    pass