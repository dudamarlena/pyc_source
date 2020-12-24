# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/1000_common_models_to_dict.py
# Compiled at: 2016-06-16 16:03:55
"""
Copyright (c) 2015 Maciej Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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


def test_to_dict_cache():
    from corecluster.cache.task import Task
    t = Task()
    t.set_prop('x', 1)
    t.set_prop('y', 2)
    d = t.to_dict
    assert 'data' in d
    assert 'type' in d
    assert 'action' in d


def test_to_dict_model():
    from corecluster.models.core import Image
    t = Image()
    t.set_prop('x', 1)
    t.set_prop('y', 2)
    d = t.to_dict
    assert 'data' in d
    assert 'type' in d
    assert 'access' in d