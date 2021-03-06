# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0003_image_transient.py
# Compiled at: 2017-01-21 08:38:36
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


def test_create():
    global image
    image_types = api.supported_image_types()
    disk_controllers = api.supported_disk_controllers()
    print image_types
    print disk_controllers
    image = api.image_create('test image', 'image description', 10485760, image_types[0], disk_controllers[0], 'private', format='qcow2')


def test_wait_created():
    for i in xrange(60):
        img = api.image_by_id(image.id)
        if img.state == 'ok':
            return
        if img.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('image not created')


def test_delete():
    image.delete()


def test_create_default_image():
    global image
    images = api.image_list()
    for image in images:
        if image.name == 'default image':
            return

    image_types = api.supported_image_types()
    disk_controllers = api.supported_disk_controllers()
    image = api.image_create('default image', 'image description', 10485760, image_types[0], disk_controllers[0], 'private', format='qcow2')
    image.upload_url('https://packages.cloudover.org/images/cirros.qcow2')


def test_wait_default_created():
    for i in xrange(60):
        img = api.image_by_id(image.id)
        if img.state == 'ok':
            return
        if img.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('image not created')


def test_create_default_image():
    global image
    images = api.image_list()
    for image in images:
        if image.name == 'xenial image':
            return

    image_types = api.supported_image_types()
    disk_controllers = api.supported_disk_controllers()
    image = api.image_create('xenial image', 'image description', 10485760, image_types[0], disk_controllers[0], 'private', format='qcow2')
    image.upload_url('https://packages.cloudover.org/images/ubuntu-xenial-cloud.qcow2')


def test_wait_default_created():
    for i in xrange(60):
        img = api.image_by_id(image.id)
        if img.state == 'ok':
            return
        if img.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('image not created')