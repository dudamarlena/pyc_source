# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/pycore/models/vm.py
# Compiled at: 2017-04-25 02:42:20
__doc__ = '\nCopyright 2014-2017 cloudover.io ltd.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated\ndocumentation files (the "Software"), to deal in the Software without restriction, including without limitation the\nrights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit\npersons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the\nSoftware.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE\nWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\nOTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
from pycore.utils import request, check_version
from pycore.models.template import Template
from pycore.models.image import Image
from pycore.models.base_model import BaseModel
from pycore.models.task import Task
from pycore.models.lease import Lease

class VM(BaseModel):

    def __init__(self, *args, **kwargs):
        super(VM, self).__init__(*args, **kwargs)
        self.template = Template(self.oc_address, self.token, self.template)
        self.base_image = Image(self.oc_address, self.token, self.base_image)
        if self.tasks is not None:
            t = []
            for task in self.tasks:
                t.append(Task(self.oc_address, self.token, task, self.debug))

            self.tasks = t
        else:
            self.tasks = []
        if self.disks is not None:
            d = []
            for disk in self.disks:
                d.append(Image(self.oc_address, self.token, disk, self.debug))

            self.disks = d
        else:
            self.disks = []
        l = []
        for lease in self.leases:
            l.append(Lease(self.oc_address, self.token, lease, self.debug))

        self.leases = l
        return

    def __str__(self):
        return self.name

    def reset(self):
        request(self.oc_address, '/api/vm/reset/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def poweroff(self):
        request(self.oc_address, '/api/vm/poweroff/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def shutdown(self):
        request(self.oc_address, '/api/vm/shutdown/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def cleanup(self):
        request(self.oc_address, '/api/vm/cleanup/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def start(self):
        request(self.oc_address, '/api/vm/start/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def resize_image(self, size):
        check_version(self.oc_address, self.token, '16.11')
        request(self.oc_address, '/api/vm/resize/', {'token': self.token, 'vm_id': self.id, 
           'size': size}, self.debug)

    def resize(self, size):
        print 'vm.resize is deprecated. use vm.resize_image'
        self.resize_image(size)

    def save_image(self):
        request(self.oc_address, '/api/vm/save_image/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def reload_image(self):
        request(self.oc_address, '/api/vm/reload_image/', {'token': self.token, 'vm_id': self.id}, self.debug)

    def cancel_tasks(self):
        for task in self.tasks:
            request(self.oc_address, '/api/task/cancel/', {'token': self.token, 'task_id': task.id}, self.debug)

    def console(self, enable):
        request(self.oc_address, '/api/vm/console/', {'token': self.token, 'vm_id': self.id, 
           'enable': enable}, self.debug)

    def edit(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
                request(self.oc_address, '/api/vm/edit/', {'token': self.token, 'vm_id': self.id, 
                   key: kwargs[key]}, self.debug)