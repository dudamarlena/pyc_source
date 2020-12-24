# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0004_vm_create.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
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
    cloud = Cloud(settings.address, settings.login, settings.password)
    api = cloud.get_api()
    templates = api.template_list()
    template = templates[0]
    images = api.image_list()
    for img in images:
        if img.name == 'default image' and img.state == 'ok':
            image = img
            return

    raise Exception('image not found')


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_vm_create():
    global vm
    vm = api.vm_create('test vm', 'vm description', template, image)


def test_wait_vm_stopped():
    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'stopped':
            break
        elif v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)


def test_vm_cleanup():
    vm.cleanup()


def test_vm_list():
    vms = api.vm_by_name(vm.name)
    assert isinstance(vms, list)
    assert len(vms) > 0
    assert api.vm_by_id(vm.id) != None
    api.vm_list()
    return


def test_wait_closed():
    for i in xrange(60):
        v = api.vm_by_id(vm.id)
        if v.state == 'closed':
            return
        if v.state == 'failed':
            raise Exception('vm failed')
        else:
            time.sleep(1)

    raise Exception('vm close timeout')