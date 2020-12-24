# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/composer/tests/test_admin.py
# Compiled at: 2017-10-20 11:35:08
from django.test import TestCase, override_settings
from composer import admin

class TestTileAdminForm(TestCase):

    @override_settings(COMPOSER={'load-existing-styles': {'greedy': True}})
    def test_existing_styles(self):
        choices = admin.TileInlineForm().fields['style'].widget.choices
        expected_choices = [
         ('3rdparty_override', '3rdparty override'),
         ('context', 'Context'),
         ('extra_style', 'Extra style'),
         ('style_for_model_one', 'Style for model one'),
         ('tile', 'Tile')]
        self.assertEqual(choices, expected_choices)

    @override_settings(COMPOSER={'load-existing-styles': {'includes': {'tests': '__all__'}}})
    def test_app_styles(self):
        choices = admin.TileInlineForm().fields['style'].widget.choices
        expected_choices = [
         ('3rdparty_override', '3rdparty override'),
         ('extra_style', 'Extra style'),
         ('style_for_model_one', 'Style for model one'),
         ('tile', 'Tile')]
        self.assertEqual(choices, expected_choices)

    @override_settings(COMPOSER={'load-existing-styles': {'excludes': {'tests': ['dummymodel2']}}})
    def test_app_excludes_styles(self):
        choices = admin.TileInlineForm().fields['style'].widget.choices
        expected_choices = [
         ('context', 'Context'),
         ('style_for_model_one', 'Style for model one'),
         ('tile', 'Tile')]
        self.assertEqual(choices, expected_choices)

    @override_settings(COMPOSER={'load-existing-styles': {'includes': {'composer': ['tile']}}})
    def test_composer__styles(self):
        choices = admin.TileInlineForm().fields['style'].widget.choices
        expected_choices = [
         ('context', 'Context'),
         ('tile', 'Tile')]
        self.assertEqual(choices, expected_choices)

    @override_settings(COMPOSER={'load-existing-styles': {'excludes': {'composer': '__all__'}}})
    def test_composer_excludes_styles(self):
        choices = admin.TileInlineForm().fields['style'].widget.choices
        expected_choices = [
         ('3rdparty_override', '3rdparty override'),
         ('extra_style', 'Extra style'),
         ('style_for_model_one', 'Style for model one'),
         ('tile', 'Tile')]
        self.assertEqual(choices, expected_choices)

    @override_settings(COMPOSER={'load-existing-styles': {'greedy': True}, 'styles': [
                ('detail', 'Detail'),
                ('context', 'Context'),
                ('extra_style', 'Extra style'),
                ('style_for_model_one', 'Style for model one')]})
    def test_duplicate_removal_styles(self):
        choices = admin.TileInlineForm().fields['style'].widget.choices
        expected_choices = [
         ('3rdparty_override', '3rdparty override'),
         ('context', 'Context'),
         ('detail', 'Detail'),
         ('extra_style', 'Extra style'),
         ('style_for_model_one', 'Style for model one'),
         ('tile', 'Tile')]
        self.assertEqual(choices, expected_choices)