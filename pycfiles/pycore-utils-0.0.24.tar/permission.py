# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/pycore/models/permission.py
# Compiled at: 2017-04-25 02:52:01
__doc__ = '\nCopyright 2014-2017 cloudover.io ltd.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated\ndocumentation files (the "Software"), to deal in the Software without restriction, including without limitation the\nrights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit\npersons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the\nSoftware.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE\nWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\nOTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
from pycore.utils import request, calc_hash
from pycore.models.base_model import BaseModel

class Permission(BaseModel):

    def __init__(self, address, login, password, seed, permission_dict, debug=False):
        self.login = login
        self.password = password
        self.oc_address = address
        self.seed = seed
        self.debug = debug
        self.token = None
        tokens = request(self.oc_address, '/user/token/get_list/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
           'name': 'pycloud'}, self.debug)
        if len(tokens) == 0:
            self.token = request(self.oc_address, '/user/token/create/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
               'name': 'pycloud'}, self.debug)['token']
        else:
            self.token = tokens[0]['token']
        BaseModel.__init__(self, self.oc_address, self.token, permission_dict)
        return

    def __str__(self):
        return self.function

    def attach(self, token):
        request(self.oc_address, '/user/permission/attach/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
           'function': self.function, 
           'token_id': token.id})

    def detach(self, token):
        request(self.oc_address, '/user/permission/detach/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
           'function': self.function, 
           'token_id': token.id})