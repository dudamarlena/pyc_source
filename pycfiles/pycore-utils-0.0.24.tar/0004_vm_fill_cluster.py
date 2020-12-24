# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0004_vm_fill_cluster.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2015 Marta Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import settings
from pycore import Cloud
import time
api = None
cloud = None
template = None
image = None

def setup_module(module):
    global api
    global cloud
    global image
    cloud = Cloud(settings.address, settings.login, settings.password, debug=True)
    api = cloud.get_api()
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


def test_fill_cluster_each_template_type():
    caps = api.template_capabilities()
    for template_id in caps.keys():
        template = api.template_by_id(template_id)
        vms = []
        for i in xrange(caps[template_id]):
            vms.append(api.vm_create('vm_%d' % i, 'capability test', template, image))

        for vm in vms:
            for i in xrange(60):
                vm_tmp = api.vm_by_id(vm.id)
                if vm_tmp.state == 'stopped':
                    break
                else:
                    time.sleep(1)

        for vm in vms:
            vm.cleanup()

        for vm in vms:
            for i in xrange(60):
                vm_tmp = api.vm_by_id(vm.id)
                if vm_tmp.state == 'closed':
                    break
                else:
                    time.sleep(1)