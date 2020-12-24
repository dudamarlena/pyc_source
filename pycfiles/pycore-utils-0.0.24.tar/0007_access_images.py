# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/0007_access_images.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import settings
from pycore import Cloud
import time
qapi = None
mapi = None
qcloud = None
mcloud = None

def setup_module(module):
    global mapi
    global mcloud
    global qapi
    global qcloud
    mcloud = Cloud(settings.address, settings.login, settings.password)
    qcloud = Cloud(settings.address, settings.additional_login, settings.additional_password)
    mapi = mcloud.get_api()
    qapi = qcloud.get_api()


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_access():
    images = qapi.image_list()
    for image in images:
        if image.name == 'default image':
            raise Exception('transient image visible in permanent list')
        elif image.name == 'permanent image':
            raise Exception('permanent image visible in transient images')


def test_delete():
    images = mapi.image_list()
    try:
        img = qapi.image_by_id(images[0].id)
        img.delete()
    except:
        return

    raise Exception('user is permitted to delete foreign images')