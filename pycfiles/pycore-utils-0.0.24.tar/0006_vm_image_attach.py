# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0006_vm_image_attach.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import settings
from pycore import Cloud
import time
api = None
cloud = None
base_image = None
permanent_image = None
template = None
vm = None
leases = None

def setup_module(module):
    global api
    global base_image
    global cloud
    global permanent_image
    global template
    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()
    templates = api.template_list()
    template = templates[0]
    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            base_image = img

    if base_image == None:
        raise Exception('base image not found')
    for img in images:
        if img.name == 'permanent image' and img.state == 'ok':
            permanent_image = img

    if permanent_image == None:
        raise Exception('permanent image not found')
    return


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_vm_create():
    global vm
    vm = api.vm_create('Isolated network test', 'vm description', template, base_image)


def test_image_attach():
    permanent_image.attach(vm)


def test_image_detach():
    permanent_image.detach(vm)


def test_image_reattach():
    permanent_image.attach(vm)
    vm.start()


def test_wait_vm():
    for i in xrange(120):
        v = api.vm_by_id(vm.id)
        if v.state == 'running':
            return
        if v.state == 'failed':
            raise Exception('image failed')
        else:
            time.sleep(1)

    raise Exception('vm create timeout')


def test_vm_cleanup():
    vm.poweroff()
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


# global leases ## Warning: Unused global