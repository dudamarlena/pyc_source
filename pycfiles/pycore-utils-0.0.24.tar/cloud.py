# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/pycore/cloud.py
# Compiled at: 2018-07-01 06:33:24
__doc__ = '\nCopyright 2014-2017 cloudover.io ltd.\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated\ndocumentation files (the "Software"), to deal in the Software without restriction, including without limitation the\nrights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit\npersons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the\nSoftware.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE\nWARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR\nCOPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR\nOTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n'
from pycore.utils import request, calc_hash
from pycore.api import Api
from pycore.models.token import Token
from pycore.models.permission import Permission
import hashlib, datetime

class Cloud:
    """
    Basic class for operations on user's account in OverCluster.
    """
    oc_address = None
    login = None
    password = None
    seed = None
    debug = False

    def __init__(self, address, login, password, debug=False):
        self.oc_address = address
        self.login = login
        self.password = password
        self.debug = debug
        self.seed = request(self.oc_address, '/user/user/get_seed/', {'login': self.login}, debug)['seed']

    def get_api(self):
        """
        Generate API object and fetch token for it's instance to manage all non-user
        functions in cloud. Api class could be generated without calling this
        function, unless you have valid token.
        """
        token = None
        password_hash = None
        try:
            password_hash = calc_hash(self.password, self.seed)
            tokens = request(self.oc_address, '/user/token/get_list/', {'login': self.login, 'pw_hash': password_hash, 
               'name': 'pycloud'}, self.debug)
        except:
            try:
                password_hash = calc_hash(self.password, self.seed, method='sha1')
                print 'Cloud.get_api: Using old, unsecure SHA1 method'
                tokens = request(self.oc_address, '/user/token/get_list/', {'login': self.login, 'pw_hash': password_hash, 
                   'name': 'pycloud'}, self.debug)
            except:
                password_hash = calc_hash(self.password, self.seed, method='legacy')
                print 'Cloud.get_api: Using old, unsecure SHA1 method with old CoreCluster API (<=16.03)'
                tokens = request(self.oc_address, '/user/token/get_list/', {'login': self.login, 'pw_hash': password_hash, 
                   'name': 'pycloud'}, self.debug)

        if len(tokens) == 0:
            token = request(self.oc_address, '/user/token/create/', {'login': self.login, 'pw_hash': password_hash, 
               'name': 'pycloud'}, self.debug)['token']
        else:
            try:
                request(self.oc_address, '/api/api/list_api_modules/', {'token': tokens[0]['token']})
                token = tokens[0]['token']
            except:
                token = request(self.oc_address, '/user/token/create/', {'login': self.login, 'pw_hash': password_hash, 
                   'name': 'pycloud'}, self.debug)['token']

        return Api(self.oc_address, token, self.debug)

    @staticmethod
    def register(address, login, password, name, surname, email, debug=False):
        """
        Register new user account
        """
        request(address, '/user/user/register/', {'login': login, 'password': password, 
           'name': name, 
           'surname': surname, 
           'email': email}, debug)
        return Cloud(address, login, password, debug)

    def token_by_id(self, token_id):
        token = request(self.oc_address, '/user/token/get/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
           'token_id': token_id}, self.debug)
        return Token(self.oc_address, self.login, self.password, self.seed, token, self.debug)

    def token_list(self):
        tokens = request(self.oc_address, '/user/token/get_list/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed)}, self.debug)
        token_list = []
        for token in tokens:
            token_list.append(Token(self.oc_address, self.login, self.password, self.seed, token, self.debug))

        return token_list

    def token_create(self, name='', token_valid_to=datetime.datetime.now() + datetime.timedelta(weeks=1)):
        token = request(self.oc_address, '/user/token/create/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
           'name': name, 
           'token_valid_to': str(token_valid_to)}, self.debug)
        return Token(self.oc_address, self.login, self.password, self.seed, token, self.debug)

    def permission_list(self):
        permissions = request(self.oc_address, '/user/permission/get_list/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed)}, self.debug)
        permission_list = []
        for permission in permissions:
            permission_list.append(Permission(self.oc_address, self.login, self.password, self.seed, permission, self.debug))

        return permission_list

    def account_info(self):
        print 'Cloud.account_info: This method is obsolete. Use account_quota'
        return self.account_quota()

    def account_quota(self):
        return request(self.oc_address, '/user/user/get_quota/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed)}, self.debug)

    def change_password(self, password):
        seed = hashlib.sha1(str(datetime.datetime.now()).encode('utf-8')).hexdigest()
        pw_hash = calc_hash(password, seed)
        try:
            request(self.oc_address, '/user/user/change_password/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed), 
               'password_hash': pw_hash, 
               'password_seed': seed}, self.debug)
        except:
            try:
                print 'Cloud.change_password: Using uld, unsecure SHA1 for authentication. Changing to SHA512 hash'
                request(self.oc_address, '/user/user/change_password/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed, method='sha1'), 
                   'password_hash': pw_hash, 
                   'password_seed': seed}, self.debug)
            except:
                print 'Cloud.change_password: Using old, unsecure SHA1 method with old CoreCluster API (<=16.03)'
                pw_hash = calc_hash(password, seed, method='legacy')
                request(self.oc_address, '/user/user/change_password/', {'login': self.login, 'pw_hash': calc_hash(self.password, self.seed, method='legacy'), 
                   'password_hash': pw_hash, 
                   'password_seed': seed}, self.debug)