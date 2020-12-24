# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0002_permissions_token.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import settings
from pycore import Cloud, Api
from pycore.utils import CloudException
api = None
cloud = None
token = None

def setup_module(module):
    global api
    global cloud
    cloud = Cloud(settings.address, settings.login, settings.password, debug=True)
    api = cloud.get_api()


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_create_token():
    global token
    token = cloud.token_create()


def test_list_permissions():
    plist = cloud.permission_list()
    for p in plist:
        if p.function.startswith('api/image') or p.function.startswith('api/api'):
            p.attach(token)


def test_call_permited_function():
    api_tok = Api(cloud.oc_address, token.token)
    api_tok.image_list()


def test_call_restricted_function():
    api_tok = Api(cloud.oc_address, token.token)
    try:
        api_tok.vm_list()
        raise Exception('function_permited')
    except CloudException as e:
        if e.status != 'token_permission':
            raise Exception('function_failed')


def test_remove_token():
    token.delete()