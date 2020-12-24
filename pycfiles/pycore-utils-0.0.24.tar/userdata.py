# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/pycore/extensions/coretalk/models/userdata.py
# Compiled at: 2018-07-01 17:50:44
__doc__ = '\nCopyright 2014-2017 cloudover.io ltd.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated\ndocumentation files (the "Software"), to deal in the Software without restriction, including without limitation the\nrights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit\npersons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the\nSoftware.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE\nWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\nOTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
from pycore.utils import request, check_version, VersionException
from pycore.models.base_model import BaseModel

class UserData(BaseModel):

    def delete(self):
        try:
            check_version(self.oc_address, self.token, '15.12')
            request(self.oc_address, '/api/userdata/delete/', {'token': self.token, 'userdata_id': self.id}, self.debug)
        except VersionException:
            request(self.oc_address, '/coreTalk/userdata/delete/', {'token': self.token, 'userdata_id': self.id}, self.debug)

    def attach(self, vm):
        try:
            check_version(self.oc_address, self.token, '15.12')
            request(self.oc_address, '/api/userdata/attach/', {'token': self.token, 'userdata_id': self.id, 
               'vm_id': vm.id}, self.debug)
        except VersionException:
            request(self.oc_address, '/coreTalk/userdata/attach/', {'token': self.token, 'userdata_id': self.id, 
               'vm_id': vm.id}, self.debug)

    def detach(self, vm):
        try:
            check_version(self.oc_address, self.token, '15.12')
            request(self.oc_address, '/api/userdata/detach/', {'token': self.token, 'vm_id': vm.id}, self.debug)
        except VersionException:
            request(self.oc_address, '/coreTalk/userdata/detach/', {'token': self.token, 'userdata_id': self.id, 
               'vm_id': vm.id}, self.debug)

    def edit(self, **kwargs):
        for key in kwargs.keys():
            if hasattr(self, key):
                setattr(self, key, kwargs[key])
                try:
                    check_version(self.oc_address, self.token, '15.12')
                    request(self.oc_address, '/api/userdata/edit/', {'token': self.token, 'userdata_id': self.id, 
                       key: kwargs[key]}, self.debug)
                except VersionException:
                    request(self.oc_address, '/coreTalk/userdata/edit/', {'token': self.token, 'userdata_id': self.id, 
                       key: kwargs[key]}, self.debug)