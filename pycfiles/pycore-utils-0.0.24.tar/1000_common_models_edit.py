# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/1000_common_models_edit.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2015 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import os, django

def setup_module(module):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'corecluster.settings'
    django.setup()


def teardown_module(module):
    pass


def setup_function(function):
    pass


def teardown_function(function):
    pass


def test_edit_editable():
    from corecluster.models.core.image import Image
    t = Image()
    t.edit(name='test')


def test_edit_non_editable():
    from corecluster.models.core.image import Image
    t = Image()
    t.id = 'a'
    try:
        t.edit(id='test')
    except:
        pass

    if t.id != 'a':
        raise Exception('Model allows to edit non editable field')


def test_edit_incorrect_value():
    from corecluster.models.core.image import Image
    t = Image()
    edited = False
    try:
        t.edit(name=None)
        edited = True
    except:
        pass

    if edited:
        raise Exception('Model allows to edit with incorrect value')
    return


def test_edit_non_existing():
    from corecluster.models.core.image import Image
    t = Image()
    try:
        t.edit(xyz=None)
    except:
        pass

    if hasattr(t, 'xyz'):
        raise Exception('Model allows to edit non existing field')
    return