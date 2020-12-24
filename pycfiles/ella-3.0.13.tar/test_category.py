# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/xaralis/Workspace/elladev/ella/test_ella/test_core/test_category.py
# Compiled at: 2013-07-03 05:00:55
from test_ella.cases import RedisTestCase as TestCase
from nose import tools
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from ella.core.models import Category
from test_ella.test_core import create_basic_categories

class TestCategory(TestCase):

    def setUp(self):
        super(TestCategory, self).setUp()
        create_basic_categories(self)

    def test_slug_cannot_start_as_publishable_url(self):
        self.category_nested.slug = '123-slug'
        tools.assert_raises(ValidationError, self.category_nested.full_clean)

    def test_slug_can_start_with_number(self):
        self.category_nested.slug = '3d-slug'
        self.category_nested.full_clean()

    def test_get_children(self):
        tools.assert_equals(['nested-category'], [ c.tree_path for c in self.category.get_children() ])

    def test_get_children_recursive(self):
        tools.assert_equals([
         'nested-category', 'nested-category/second-nested-category'], [ c.tree_path for c in self.category.get_children(recursive=True) ])

    def test_proper_root_path(self):
        tools.assert_equals('', self.category.tree_path)

    def test_proper_firstlevel_path(self):
        tools.assert_equals('nested-category', self.category_nested.tree_path)

    def test_category_rename_tree_path(self):
        self.category_nested.slug = 'new-nested-category'
        self.category_nested.save()
        tools.assert_equals('new-nested-category', self.category_nested.tree_path)

    def test_proper_secondlevel_path(self):
        tools.assert_equals('nested-category/second-nested-category', self.category_nested_second.tree_path)

    def test_category_rename_children(self):
        self.category_nested.slug = 'new-nested-category'
        self.category_nested.save()
        category_nested_second = Category.objects.get(pk=self.category_nested_second.pk)
        tools.assert_equals('new-nested-category/second-nested-category', category_nested_second.tree_path)

    def test_proper_parent(self):
        tools.assert_equals(self.category, self.category_nested.tree_parent)

    def test_main_parent_nested_second_level(self):
        tools.assert_equals(self.category_nested, self.category_nested_second.get_root_category())

    def test_main_parent_nested(self):
        tools.assert_equals(self.category_nested, self.category_nested.get_root_category())

    def test_main_parent_nested_third(self):
        category_nested_third = Category.objects.create(title='Third nested category', description='category nested in self.category_nested_second', tree_parent=self.category_nested_second, site_id=self.site_id, slug='third-nested-category')
        tools.assert_equals(self.category_nested, category_nested_third.get_root_category())

    def test_root_url(self):
        url = reverse('root_homepage')
        tools.assert_equals(url, self.category.get_absolute_url())

    def test_category_url(self):
        url = reverse('category_detail', args=(self.category_nested.tree_path,))
        tools.assert_equals(url, self.category_nested.get_absolute_url())