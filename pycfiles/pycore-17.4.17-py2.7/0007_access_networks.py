# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0007_access_networks.py
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
qapi = None
mapi = None
qcloud = None
mcloud = None
network = None

def setup_module(module):
    global mapi
    global mcloud
    global network
    global qapi
    global qcloud
    mcloud = Cloud(settings.address, settings.login, settings.password)
    qcloud = Cloud(settings.address, settings.additional_login, settings.additional_password)
    mapi = mcloud.get_api()
    qapi = qcloud.get_api()
    network = qapi.network_create(26, 'Q', False)


def teardown_module(module):
    network.delete()


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_get():
    try:
        mapi.network_by_id(network.id)
    except:
        return

    raise Exception('Network is accessible for other accounts')