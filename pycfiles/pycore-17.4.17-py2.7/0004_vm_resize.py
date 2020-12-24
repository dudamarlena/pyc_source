# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0004_vm_resize.py
# Compiled at: 2016-12-29 17:24:33
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
image = None
template = None
vm = None

def setup_module(module):
    global api
    global cloud
    global image
    global template
    global vm
    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()
    templates = api.template_list()
    template = templates[0]
    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            image = img
            break

    if image == None:
        raise Exception('image not found')
    vm = api.vm_create('test vm', 'vm description', template, image)
    return


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_wait_vm_created():
    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'stopped':
            return
        if v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)

    raise Exception('vm create timeout')


def test_vm_resize_negative():
    try:
        vm.resize_image(-1)
    except:
        return

    raise Exception('Negative image size accepted')


def test_vm_resize_too_large():
    try:
        vm.resize_image(vm.template.hdd * 1024 * 1024 + 1)
    except:
        return

    raise Exception('Too large image size accepted')


def test_vm_resize():
    vm.resize_image(vm.template.hdd)


def test_vm_poweroff():
    vm.poweroff()


def test_wait_vm_powered_off():
    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'stopped':
            return
        if v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)

    raise Exception('vm poweroff timeout')


def test_vm_cleanup():
    vm.cleanup()


def test_wait_closed():
    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'closed':
            return
        if v.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('vm close timeout')