# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-storymarket/tests/test_categories.py
# Compiled at: 2010-07-12 12:21:40
from __future__ import absolute_import
from storymarket import Category
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api
sm = FakeStorymarket()

def test_list_categories():
    assert_list_api(sm, sm.categories.all, Category, 'content/category/')


def test_list_subcategories():
    assert_list_api(sm, sm.subcategories.all, Category, 'content/sub_category/')


def test_get_category():
    assert_get_api(sm, sm.categories.get, Category, 'content/category/1/')


def test_get_subcategory():
    assert_get_api(sm, sm.subcategories.get, Category, 'content/sub_category/1/')