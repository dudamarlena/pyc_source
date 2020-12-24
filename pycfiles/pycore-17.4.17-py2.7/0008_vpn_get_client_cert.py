# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0008_vpn_get_client_cert.py
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
import time
api = None
cloud = None
vpn = None

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


def test_vpn_create():
    global vpn
    vpn = api.vpn.create('test')


def test_vpn_wait():
    n = 0
    while n < 60:
        vpns = api.vpn.get_list()
        for v in vpns:
            if v.id == vpn.id:
                if v.state == 'running':
                    return
                if v.state == 'failed':
                    raise Exception('vpn failed')
                else:
                    time.sleep(1)

        n = n + 1


def test_vpn_client_cert():
    certs = vpn.client_cert()
    assert 'key' in certs
    assert 'cert' in certs
    assert 'ca_cert' in certs


def test_vpn_delete():
    vpn.delete()