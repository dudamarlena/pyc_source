# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0002_account_network_quota.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import math, settings
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


def test_routed_lease_in_quota():
    quota = cloud.account_quota()
    mask = int(32 - math.floor(math.log(int(quota['routed_lease_quota']) * 4, 2)))
    net = api.network_create(name='in', mask=mask, mode='routed')
    net.delete()


def test_routed_lease_over_quota():
    quota = cloud.account_quota()
    try:
        mask = int(32 - math.floor(math.log(int(quota['routed_lease_quota']) * 4, 2)) - 1)
        net = api.network_create(name='in', mask=mask, mode='routed')
        net.delete()
    except:
        return

    raise Exception('network over quota allowed')


def test_public_lease_in_quota():
    quota = cloud.account_quota()
    mask = int(32 - math.floor(math.log(int(quota['public_lease_quota']), 2)))
    net = api.network_create(name='in', mask=mask, mode='public')
    net.delete()


def test_routed_public_over_quota():
    quota = cloud.account_quota()
    try:
        mask = int(32 - math.floor(math.log(int(quota['public_lease_quota']), 2)) - 1)
        net = api.network_create(name='in', mask=mask, mode='public')
        net.delete()
    except:
        return

    raise Exception('network over quota allowed')


def test_isolated_network_quota():
    networks = []
    quota = cloud.account_quota()
    for i in xrange(int(quota['isolated_network_quota'])):
        networks.append(api.network_create(name='isolated%d' % i, mask=24, mode='isolated', address='10.0.0.0'))

    try:
        api.network_create(name='isolated%d' % i, mask=24, mode='isolated', address='10.0.0.0')
        raise Exception('done')
    except CloudException:
        pass
    except:
        raise Exception('isolated network over quota allowed')

    for net in networks:
        net.delete()


def routed_lease_over_quota():
    quota = cloud.account_quota()
    try:
        mask = int(32 - math.floor(math.log(int(quota['routed_lease_quota']), 2)))
        net = api.network_create(name='in', mask=mask, mode='routed')
        net.delete()
    except:
        return

    raise Exception('network over quota allowed')