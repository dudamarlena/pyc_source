# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/1000_common_models_set_prop.py
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


def test_set_prop_cache():
    from corecluster.cache.task import Task
    t = Task()
    t.set_prop('x', 1)
    t.set_prop('y', 2)
    assert t.get_prop('x') == 1
    assert t.get_prop('y') == 2
    t.set_all_props({'a': 1, 'b': 2})
    props = t.get_all_props()
    assert 'a' in props
    assert 'b' in props
    assert 'x' not in props
    assert 'y' not in props


def test_set_prop_model():
    from corecluster.models.core.image import Image
    t = Image()
    t.set_prop('x', 1)
    t.set_prop('y', 2)
    assert t.get_prop('x') == 1
    assert t.get_prop('y') == 2
    t.set_all_props({'a': 1, 'b': 2})
    props = t.get_all_props()
    assert 'a' in props
    assert 'b' in props
    assert 'x' not in props
    assert 'y' not in props