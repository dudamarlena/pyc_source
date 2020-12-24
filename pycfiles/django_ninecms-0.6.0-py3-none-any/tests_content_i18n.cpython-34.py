# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/rabelvideo/ninecms/tests/tests_content_i18n.py
# Compiled at: 2015-11-03 08:29:58
# Size of source mod 2**32: 4567 bytes
"""
Tests declaration for Nine CMS

All tests assume settings.LANGUAGE_CODE is defined
"""
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.utils import translation
from django.conf import settings
from ninecms.tests.setup import get_second_language, create_front, create_basic, create_block_static, create_menu, create_block_menu, assert_front, assert_basic, assert_menu

class ContentI18nTests(TestCase):
    __doc__ = ' Tests with default initial content, i18n, no login '

    @classmethod
    def setUpTestData(cls):
        """ Setup initial data:
        Create 2 front pages
        Create 2 basic pages
        :return: None
        """
        cls.second_lang = get_second_language()
        cls.node_rev_front_first = create_front('/', settings.LANGUAGE_CODE)
        cls.node_rev_front_sec = create_front('/', cls.second_lang)
        cls.node_rev_basic_first = create_basic('about', settings.LANGUAGE_CODE)
        cls.node_rev_basic_sec = create_basic('about', cls.second_lang)
        for i in range(0, 3):
            node_rev_basic_first = create_basic('block/' + str(i), settings.LANGUAGE_CODE, '1st lang ' + str(i))
            node_rev_basic_second = create_basic('block/' + str(i), cls.second_lang, '2nd lang ' + str(i))
            create_block_static(cls.node_rev_front_first.node.page_type, node_rev_basic_first.node)
            create_block_static(cls.node_rev_front_first.node.page_type, node_rev_basic_second.node)

        cls.menu_en = create_menu('en')
        cls.menu_el = create_menu('el')
        create_block_menu(cls.node_rev_front_first.node.page_type, cls.menu_en)
        create_block_menu(cls.node_rev_front_first.node.page_type, cls.menu_el)

    def test_node_model_methods(self):
        """ Test model methods
        :return: None
        """
        lang = ''
        if settings.I18N_URLS:
            lang = '/' + settings.LANGUAGE_CODE
        self.assertEqual(str(self.node_rev_front_first.node.get_absolute_url()), lang + '/')
        self.assertEqual(str(self.node_rev_basic_first.node.get_absolute_url()), lang + '/about/')

    def test_node_view_with_front_i18n(self):
        """ Test front page with multiple languages
        :return: None
        """
        translation.activate(settings.LANGUAGE_CODE)
        assert_front(self, reverse('ninecms:index'))
        translation.activate(self.second_lang)
        assert_front(self, reverse('ninecms:index'), self.second_lang)

    def test_node_view_with_basic_i18n(self):
        """ Test basic page with multiple languages
        :return: None
        """
        assert_basic(self, 'about/')
        assert_basic(self, 'about/', 'alias', self.second_lang)

    def test_node_view_block_static_i18n(self):
        """ Test static block for i18n front view
        Change in v0.2: require block for each language
        :return: None
        """
        translation.activate(settings.LANGUAGE_CODE)
        response = assert_front(self, reverse('ninecms:index'))
        for i in range(0, 3):
            self.assertContains(response, '<div class="body">1st lang  ' + str(i) + ' page.</div>', html=True)
            if settings.I18N_URLS:
                self.assertNotContains(response, '<div class="body">2nd lang  ' + str(i) + ' page.</div>', html=True)
                continue

        translation.activate(self.second_lang)
        response = assert_front(self, reverse('ninecms:index'), self.second_lang)
        for i in range(0, 3):
            if settings.I18N_URLS:
                self.assertNotContains(response, '<div class="body">1st lang  ' + str(i) + ' page.</div>', html=True)
            self.assertContains(response, '<div class="body">2nd lang  ' + str(i) + ' page.</div>', html=True)

    def test_node_view_block_menu_i18n(self):
        """ Test menu block for i18n front view
        :return: None
        """
        translation.activate(settings.LANGUAGE_CODE)
        response = assert_front(self, reverse('ninecms:index'))
        assert_menu(self, response)
        translation.activate(self.second_lang)
        response = assert_front(self, reverse('ninecms:index'), self.second_lang)
        assert_menu(self, response, self.second_lang)