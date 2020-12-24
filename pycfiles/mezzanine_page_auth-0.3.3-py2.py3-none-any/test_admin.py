# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/simo/PycharmProjects/mezzanine_page_auth/mezzanine_page_auth/tests/test_admin.py
# Compiled at: 2014-07-01 03:21:57
from __future__ import unicode_literals
from mock import patch, Mock
from django.contrib.admin import AdminSite
from django.contrib.messages import INFO
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory
from mezzanine.pages.models import RichTextPage, Link
from ..models import PageAuthGroup
from ..admin import PageAuthGroupAdmin, LinkAuthGroupAdmin
from .factories import UserF, GroupF, RichTextPageF, LinkF

class PageAuthGroupAdminMixinSaveRelatedTest(TestCase):

    def setUp(self):
        self.user = UserF()
        self.prefix_url = b'admin:pages_richtextpage_'
        self.factory = RequestFactory()
        self.mock_form = Mock()
        self.mock_form_formset = Mock()
        self.parent_page = RichTextPageF()
        [ PageAuthGroup.objects.create(page=self.parent_page, group=GroupF()) for i in range(0, 3)
        ]

    def tearDown(self):
        self.mock_form.reset_mock()
        self.mock_form_formset.reset_mock()

    def get_request(self, viewname, args=None, kwargs=None, query_string=None):
        url = reverse(viewname, args=args, kwargs=kwargs)
        if query_string:
            url += b'?' + query_string
        return self.factory.get(url)

    @patch(b'mezzanine_page_auth.admin.PageAuthGroupAdmin.message_user')
    @patch(b'mezzanine_page_auth.admin.PageAdmin.save_related')
    def test_add_page_with_parent_and_without_pag_inserted(self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and without PageAuthGroup inserted
        set related PageAuthGroup objects as parent
        """
        page_admin = PageAuthGroupAdmin(RichTextPage, AdminSite())
        page = RichTextPageF()
        page.parent = self.parent_page
        page.save()
        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + b'add', query_string=(b'parent={}').format(self.parent_page.pk))
        page_admin.save_related(request, self.mock_form, self.mock_form_formset, False)
        mock_save_related.assert_called_once_with(request, self.mock_form, self.mock_form_formset, False)
        self.assertListEqual(sorted(self.parent_page.pageauthgroup_set.values_list(b'group_id', flat=True)), sorted(page.pageauthgroup_set.values_list(b'group_id', flat=True)))
        mock_message_user.assert_called_once_with(request, (b'The {} "{}" has inherited the authorizations from parent "{}"').format(page._meta.verbose_name, page.title, self.parent_page.title), INFO)

    @patch(b'mezzanine_page_auth.admin.PageAuthGroupAdmin.message_user')
    @patch(b'mezzanine_page_auth.admin.PageAdmin.save_related')
    def test_add_page_with_parent_and_with_pag_inserted(self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and with PageAuthGroup inserted
        not set related PageAuthGroup objects as parent
        """
        page_admin = PageAuthGroupAdmin(RichTextPage, AdminSite())
        page = RichTextPageF()
        page.parent = self.parent_page
        page.save()
        pags_page = [ PageAuthGroup.objects.create(page=page, group=GroupF()) for i in range(0, 2)
                    ]
        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + b'add', query_string=(b'parent={}').format(self.parent_page.pk))
        with patch(b'mezzanine_page_auth.admin.PageAuthGroup.objects.create') as (mock_create):
            page_admin.save_related(request, self.mock_form, self.mock_form_formset, False)
            mock_save_related.assert_called_once_with(request, self.mock_form, self.mock_form_formset, False)
            self.assertListEqual(sorted([ pag.group_id for pag in pags_page ]), sorted(page.pageauthgroup_set.values_list(b'group_id', flat=True)))
            self.assertFalse(mock_message_user.called)
            self.assertFalse(mock_create.called)

    @patch(b'mezzanine_page_auth.admin.LinkAuthGroupAdmin.message_user')
    @patch(b'mezzanine_page_auth.admin.PageAdmin.save_related')
    def test_add_link_with_parent_and_without_pag_inserted(self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and without PageAuthGroup inserted
        set related PageAuthGroup objects as parent
        """
        page_admin = LinkAuthGroupAdmin(Link, AdminSite())
        page = LinkF()
        page.parent = self.parent_page
        page.save()
        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + b'add', query_string=(b'parent={}').format(self.parent_page.pk))
        page_admin.save_related(request, self.mock_form, self.mock_form_formset, False)
        mock_save_related.assert_called_once_with(request, self.mock_form, self.mock_form_formset, False)
        self.assertListEqual(sorted(self.parent_page.pageauthgroup_set.values_list(b'group_id', flat=True)), sorted(page.pageauthgroup_set.values_list(b'group_id', flat=True)))
        mock_message_user.assert_called_once_with(request, (b'The {} "{}" has inherited the authorizations from parent "{}"').format(page._meta.verbose_name, page.title, self.parent_page.title), INFO)

    @patch(b'mezzanine_page_auth.admin.LinkAuthGroupAdmin.message_user')
    @patch(b'mezzanine_page_auth.admin.LinkAdmin.save_related')
    def test_add_link_with_parent_and_with_pag_inserted(self, mock_save_related, mock_message_user):
        """
        save_related() on adding page and with PageAuthGroup inserted
        not set related PageAuthGroup objects as parent
        """
        page_admin = LinkAuthGroupAdmin(Link, AdminSite())
        page = LinkF()
        page.parent = self.parent_page
        page.save()
        pags_page = [ PageAuthGroup.objects.create(page=page, group=GroupF()) for i in range(0, 2)
                    ]
        self.mock_form.instance = page
        request = self.get_request(self.prefix_url + b'add', query_string=(b'parent={}').format(self.parent_page.pk))
        with patch(b'mezzanine_page_auth.admin.PageAuthGroup.objects.create') as (mock_create):
            page_admin.save_related(request, self.mock_form, self.mock_form_formset, False)
            mock_save_related.assert_called_once_with(request, self.mock_form, self.mock_form_formset, False)
            self.assertListEqual(sorted([ pag.group_id for pag in pags_page ]), sorted(page.pageauthgroup_set.values_list(b'group_id', flat=True)))
            self.assertFalse(mock_message_user.called)
            self.assertFalse(mock_create.called)