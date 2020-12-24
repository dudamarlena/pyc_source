# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/test_review_request_draft.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import print_function, unicode_literals
from django.contrib import auth
from django.contrib.auth.models import Permission, User
from django.core import mail
from django.utils import six
from djblets.testing.decorators import add_fixtures
from djblets.webapi.errors import INVALID_FORM_DATA, PERMISSION_DENIED
from djblets.webapi.testing.decorators import webapi_test_template
from kgb import SpyAgency
from reviewboard.accounts.backends import AuthBackend, StandardAuthBackend
from reviewboard.accounts.models import LocalSiteProfile
from reviewboard.changedescs.models import ChangeDescription
from reviewboard.reviews.fields import BaseEditableField, BaseTextAreaField, BaseReviewRequestField, get_review_request_fieldset
from reviewboard.reviews.models import ReviewRequest, ReviewRequestDraft
from reviewboard.reviews.signals import review_request_published, review_request_publishing
from reviewboard.webapi.errors import COMMIT_ID_ALREADY_EXISTS, NOTHING_TO_PUBLISH
from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import review_request_draft_item_mimetype
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin
from reviewboard.webapi.tests.urls import get_review_request_draft_url

@six.add_metaclass(BasicTestsMetaclass)
class ResourceTests(SpyAgency, ExtraDataListMixin, ExtraDataItemMixin, BaseWebAPITestCase):
    """Testing the ReviewRequestDraftResource API tests."""
    fixtures = [
     b'test_users']
    sample_api_url = b'review-requests/<id>/draft/'
    resource = resources.review_request_draft

    def compare_item(self, item_rsp, draft):
        changedesc = draft.changedesc
        self.assertEqual(item_rsp[b'description'], draft.description)
        self.assertEqual(item_rsp[b'testing_done'], draft.testing_done)
        self.assertEqual(item_rsp[b'extra_data'], draft.extra_data)
        self.assertEqual(item_rsp[b'changedescription'], changedesc.text)
        if changedesc.rich_text:
            self.assertEqual(item_rsp[b'changedescription_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'changedescription_text_type'], b'plain')
        if draft.description_rich_text:
            self.assertEqual(item_rsp[b'description_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'description_text_type'], b'plain')
        if draft.testing_done_rich_text:
            self.assertEqual(item_rsp[b'testing_done_text_type'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'testing_done_text_type'], b'plain')

    def setup_basic_delete_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        ReviewRequestDraft.create(review_request)
        return (
         get_review_request_draft_url(review_request, local_site_name),
         [
          review_request])

    def check_delete_result(self, user, review_request):
        self.assertIsNone(review_request.get_draft())

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        draft = ReviewRequestDraft.create(review_request)
        return (
         get_review_request_draft_url(review_request, local_site_name),
         review_request_draft_item_mimetype,
         draft)

    def test_get_with_markdown_and_force_text_type_markdown(self):
        """Testing the GET review-requests/<id>/draft/ API
        with *_text_type=markdown and ?force-text-type=markdown
        """
        self._test_get_with_force_text_type(text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'markdown', expected_text=b'\\# `This` is a **test**')

    def test_get_with_markdown_and_force_text_type_plain(self):
        """Testing the GET review-requests/<id>/draft/ API
        with *_text_type=markdown and ?force-text-type=plain
        """
        self._test_get_with_force_text_type(text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'plain', expected_text=b'# `This` is a **test**')

    def test_get_with_markdown_and_force_text_type_html(self):
        """Testing the GET review-requests/<id>/draft/ API
        with *_text_type=markdown and ?force-text-type=html
        """
        self._test_get_with_force_text_type(text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'html', expected_text=b'<p># <code>This</code> is a <strong>test</strong></p>')

    def test_get_with_plain_and_force_text_type_markdown(self):
        """Testing the GET review-requests/<id>/draft/ API
        with *_text_type=plain and ?force-text-type=markdown
        """
        self._test_get_with_force_text_type(text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'markdown', expected_text=b'\\#<\\`This\\` is a \\*\\*test\\*\\*>')

    def test_get_with_plain_and_force_text_type_plain(self):
        """Testing the GET review-requests/<id>/draft/ API
        with *_text_type=plain and ?force-text-type=plain
        """
        self._test_get_with_force_text_type(text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'plain', expected_text=b'#<`This` is a **test**>')

    def test_get_with_plain_and_force_text_type_html(self):
        """Testing the GET review-requests/<id>/draft/ API
        with *_text_type=plain and ?force-text-type=html
        """
        self._test_get_with_force_text_type(text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'html', expected_text=b'#&lt;`This` is a **test**&gt;')

    def test_get_with_markdown_and_force_markdown_and_custom_markdown(self):
        """Testing the GET review-requests/<id>/draft/ API with rich text,
        ?force-text-type=raw,markdown, and custom field that supports markdown
        """
        self._test_get_with_custom_and_force(source_text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'markdown', expected_text=b'\\# `This` is a **test**', custom_field_supports_markdown=True)

    def test_get_with_markdown_and_force_plain_and_custom_markdown(self):
        """Testing the GET review-requests/<id>/draft/ API with rich text,
        ?force-text-type=raw,plain, and custom field that supports markdown
        """
        self._test_get_with_custom_and_force(source_text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'plain', expected_text=b'# `This` is a **test**', custom_field_supports_markdown=True)

    def test_get_with_markdown_and_force_html_and_custom_markdown(self):
        """Testing the GET review-requests/<id>/draft/ API with rich text,
        ?force-text-type=raw,html, and custom field that supports markdown
        """
        self._test_get_with_custom_and_force(source_text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'html', expected_text=b'<p># <code>This</code> is a <strong>test</strong></p>', custom_field_supports_markdown=True)

    def test_get_with_markdown_and_force_markdown_and_custom_nomarkdown(self):
        """Testing the GET review-requests/<id>/draft/ API with rich text,
        ?force-text-type=raw,markdown, and custom field that does not support
        markdown
        """
        self._test_get_with_custom_and_force(source_text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'markdown', expected_text=b'\\# `This` is a **test**', custom_field_supports_markdown=False)

    def test_get_with_markdown_and_force_plain_and_custom_nomarkdown(self):
        """Testing the GET review-requests/<id>/draft/ API with rich text,
        ?force-text-type=raw,plain, and custom field that does not support
        markdown
        """
        self._test_get_with_custom_and_force(source_text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'plain', expected_text=b'# `This` is a **test**', custom_field_supports_markdown=False)

    def test_get_with_markdown_and_force_html_and_custom_nomarkdown(self):
        """Testing the GET review-requests/<id>/draft/ API with rich text,
        ?force-text-type=raw,html, and custom field that does not support
        markdown
        """
        self._test_get_with_custom_and_force(source_text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'html', expected_text=b'<p># <code>This</code> is a <strong>test</strong></p>', custom_field_supports_markdown=False)

    def test_get_with_plain_and_force_markdown_and_custom_nomarkdown(self):
        """Testing the GET review-requests/<id>/draft/ API with plain text,
        ?force-text-type=raw,markdown, and custom field that does not support
        markdown
        """
        self._test_get_with_custom_and_force(source_text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'markdown', expected_text=b'\\#<\\`This\\` is a \\*\\*test\\*\\*>', custom_field_supports_markdown=False)

    def test_get_with_plain_and_force_plain_and_custom_nomarkdown(self):
        """Testing the GET review-requests/<id>/draft/ API with plain text,
        ?force-text-type=raw,markdown, and custom field that does not support
        markdown
        """
        self._test_get_with_custom_and_force(source_text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'plain', expected_text=b'#<`This` is a **test**>', custom_field_supports_markdown=False)

    def test_get_with_plain_and_force_html_and_custom_nomarkdown(self):
        """Testing the GET review-requests/<id>/draft/ API with plain text,
        ?force-text-type=raw,markdown, and custom field that does not support
        markdown
        """
        self._test_get_with_custom_and_force(source_text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'html', expected_text=b'#&lt;`This` is a **test**&gt;', custom_field_supports_markdown=False)

    def setup_basic_post_test(self, user, with_local_site, local_site_name, post_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        return (
         get_review_request_draft_url(review_request, local_site_name),
         review_request_draft_item_mimetype, {b'description': b'New description'},
         [
          review_request])

    def check_post_result(self, user, rsp, review_request):
        draft = review_request.get_draft()
        self.assertIsNotNone(draft)
        self.assertFalse(draft.rich_text)
        self.compare_item(rsp[b'draft'], draft)

    def test_post_with_publish_and_custom_field(self):
        """Testing the POST review-requests/<id>/draft/ API with custom
        field set in same request and public=1
        """

        class CustomField(BaseReviewRequestField):
            can_record_change_entry = True
            field_id = b'my-test'

        fieldset = get_review_request_fieldset(b'info')
        fieldset.add_field(CustomField)
        try:
            review_request = self.create_review_request(submitter=self.user, publish=True, target_people=[self.user])
            rsp = self.api_post(get_review_request_draft_url(review_request), {b'extra_data.my-test': 123, 
               b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            review_request = ReviewRequest.objects.get(pk=review_request.id)
            self.assertIn(b'my-test', review_request.extra_data)
            self.assertEqual(review_request.extra_data[b'my-test'], 123)
            self.assertTrue(review_request.public)
        finally:
            fieldset.remove_field(CustomField)

    def test_post_with_publish_and_custom_field_and_unbound_extra_data(self):
        """Testing the POST review-requests/<id>/draft/ API with custom
        text field and extra_data unbound to a field set in same request and
        public=1
        """

        class CustomField(BaseTextAreaField):
            field_id = b'my-test'

        fieldset = get_review_request_fieldset(b'info')
        fieldset.add_field(CustomField)
        try:
            review_request = self.create_review_request(submitter=self.user, publish=True, target_people=[self.user])
            rsp = self.api_post(get_review_request_draft_url(review_request), {b'extra_data.my-test': b'foo', 
               b'extra_data.my-test_text_type': b'markdown', 
               b'extra_data.unbound': 42, 
               b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            draft_rsp = rsp[b'draft']
            draft_extra_data = draft_rsp[b'extra_data']
            self.assertIn(b'my-test', draft_extra_data)
            self.assertEqual(draft_extra_data[b'my-test'], b'foo')
            self.assertIn(b'unbound', draft_extra_data)
            self.assertEqual(draft_extra_data[b'unbound'], 42)
            self.assertIn(b'my-test_text_type', draft_extra_data)
            self.assertEqual(draft_extra_data[b'my-test_text_type'], b'markdown')
            review_request = ReviewRequest.objects.get(pk=review_request.id)
            self.assertIn(b'my-test', review_request.extra_data)
            self.assertEqual(review_request.extra_data[b'my-test'], b'foo')
            self.assertNotIn(b'unbound', review_request.extra_data)
            self.assertIn(b'my-test_text_type', review_request.extra_data)
            self.assertEqual(review_request.extra_data[b'my-test_text_type'], b'markdown')
            self.assertTrue(review_request.public)
        finally:
            fieldset.remove_field(CustomField)

    def test_post_with_publish_with_first_draft_as_other_user(self):
        """Testing the POST review-requests/<id>/draft/ API with first draft
        as other user (with can_edit_reviewrequest after submit-as)
        """
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(self.user, user)
        self.user.user_permissions.add(Permission.objects.get(codename=b'can_edit_reviewrequest'))
        review_request = self.create_review_request(submitter=user, target_people=[
         user])
        self.spy_on(review_request_publishing.send)
        self.spy_on(review_request_published.send)
        rsp = self.api_post(get_review_request_draft_url(review_request), {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertTrue(review_request.public)
        self.assertTrue(review_request_publishing.send.called_with(sender=ReviewRequest, user=user))
        self.assertTrue(review_request_published.send.called_with(sender=ReviewRequest, user=user))

    def test_post_with_publish_with_publish_as_owner(self):
        """Testing the POST review-requests/<id>/draft/ API with
        publish_as_owner=
        """
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(self.user, user)
        self.user.user_permissions.add(Permission.objects.get(codename=b'can_edit_reviewrequest'))
        review_request = self.create_review_request(submitter=user, publish=True, target_people=[
         user])
        self.spy_on(review_request_publishing.send)
        self.spy_on(review_request_published.send)
        rsp = self.api_post(get_review_request_draft_url(review_request), {b'summary': b'New summary', 
           b'public': True, 
           b'publish_as_owner': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertEqual(review_request.summary, b'New summary')
        self.assertTrue(review_request.public)
        self.assertTrue(review_request_publishing.send.called_with(sender=ReviewRequest, user=user))
        self.assertTrue(review_request_published.send.called_with(sender=ReviewRequest, user=user))

    def setup_basic_put_test(self, user, with_local_site, local_site_name, put_valid_data):
        review_request = self.create_review_request(with_local_site=with_local_site, submitter=user, publish=True)
        draft = ReviewRequestDraft.create(review_request)
        return (
         get_review_request_draft_url(review_request, local_site_name),
         review_request_draft_item_mimetype, {b'description': b'New description'},
         draft,
         [
          review_request])

    def check_put_result(self, user, item_rsp, draft, review_request):
        draft = ReviewRequestDraft.create(review_request)
        self.compare_item(item_rsp, draft)

    def test_put_with_no_changes(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with no changes made to the fields
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'public': True}, expected_status=NOTHING_TO_PUBLISH.http_status)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], NOTHING_TO_PUBLISH.code)
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    def test_put_with_text_type_markdown(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with legacy text_type=markdown
        """
        self._test_put_with_text_types(text_type_field=b'text_type', text_type_value=b'markdown', expected_change_text_type=b'markdown', expected_description_text_type=b'markdown', expected_testing_done_text_type=b'markdown', expected_custom_field_text_type=b'markdown', expected_changedesc_update_fields=[
         b'rich_text'], expected_draft_update_fields=[
         b'description_rich_text',
         b'testing_done_rich_text'])

    def test_put_with_text_type_plain(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with legacy text_type=plain
        """
        self._test_put_with_text_types(text_type_field=b'text_type', text_type_value=b'plain', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'plain', expected_changedesc_update_fields=[
         b'rich_text'], expected_draft_update_fields=[
         b'description_rich_text',
         b'testing_done_rich_text'])

    def test_put_with_changedescription_text_type_markdown(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with changedescription_text_type=markdown
        """
        self._test_put_with_text_types(text_type_field=b'changedescription_text_type', text_type_value=b'markdown', expected_change_text_type=b'markdown', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'markdown', expected_changedesc_update_fields=[
         b'rich_text'])

    def test_put_with_changedescription_text_type_plain(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with changedescription_text_type=plain
        """
        self._test_put_with_text_types(text_type_field=b'changedescription_text_type', text_type_value=b'plain', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'markdown', expected_changedesc_update_fields=[
         b'rich_text'])

    def test_put_with_description_text_type_markdown(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with description_text_type=markdown
        """
        self._test_put_with_text_types(text_type_field=b'description_text_type', text_type_value=b'markdown', expected_change_text_type=b'plain', expected_description_text_type=b'markdown', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'markdown', expected_draft_update_fields=[
         b'description_rich_text'])

    def test_put_with_description_text_type_plain(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with description_text_type=plain
        """
        self._test_put_with_text_types(text_type_field=b'description_text_type', text_type_value=b'plain', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'markdown', expected_draft_update_fields=[
         b'description_rich_text'])

    def test_put_with_testing_done_text_type_markdown(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with testing_done_text_type=markdown
        """
        self._test_put_with_text_types(text_type_field=b'testing_done_text_type', text_type_value=b'markdown', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'markdown', expected_custom_field_text_type=b'markdown', expected_draft_update_fields=[
         b'testing_done_rich_text'])

    def test_put_with_testing_done_text_type_plain(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with testing_done_text_type=plain
        """
        self._test_put_with_text_types(text_type_field=b'testing_done_text_type', text_type_value=b'plain', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'markdown', expected_draft_update_fields=[
         b'testing_done_rich_text'])

    def test_put_with_custom_field_text_type_markdown(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with extra_data.*_text_type=markdown
        """
        self._test_put_with_text_types(text_type_field=b'extra_data.mytext_text_type', text_type_value=b'markdown', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'markdown')

    def test_put_with_custom_field_text_type_plain(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with extra_data.*_text_type=plain
        """
        self._test_put_with_text_types(text_type_field=b'extra_data.mytext_text_type', text_type_value=b'plain', expected_change_text_type=b'plain', expected_description_text_type=b'plain', expected_testing_done_text_type=b'plain', expected_custom_field_text_type=b'plain')

    @webapi_test_template
    def test_put_with_branch(self):
        """Testing the PUT <URL> API with branch field"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'branch': b'new branch'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'branch'], b'new branch')
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(draft.branch, b'new branch')
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'branch', b'last_updated']))

    @webapi_test_template
    def test_put_with_bugs_closed(self):
        """Testing the PUT <URL> API with bugs_closed field"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'bugs_closed': b'10,20, 300,,'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'bugs_closed'], [b'10', b'20', b'300'])
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(draft.get_bug_list(), [b'10', b'20', b'300'])
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'bugs_closed', b'last_updated']))

    @webapi_test_template
    def test_put_with_changedescription(self):
        """Testing the PUT <URL> with a change description"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        changedesc = b'This is a test change description.'
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'changedescription': changedesc}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'changedescription'], changedesc)
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertIsNotNone(draft.changedesc)
        self.assertEqual(draft.changedesc.text, changedesc)
        self.assertTrue(ChangeDescription.save.last_called_with(update_fields=[
         b'text']))
        self.assertFalse(ReviewRequestDraft.save.called)

    def test_put_with_commit_id(self):
        """Testing the PUT review-requests/<id>/draft/ API with commit_id"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        commit_id = b'abc123'
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'commit_id': commit_id}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'commit_id'], commit_id)
        self.assertEqual(rsp[b'draft'][b'summary'], review_request.summary)
        self.assertEqual(rsp[b'draft'][b'description'], review_request.description)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertNotEqual(review_request.commit_id, commit_id)
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'commit_id', b'last_updated']))

    def test_put_with_commit_id_and_used_in_review_request(self):
        """Testing the PUT review-requests/<id>/draft/ API with commit_id
        used in another review request
        """
        commit_id = b'abc123'
        self.create_review_request(submitter=self.user, commit_id=commit_id, publish=True)
        review_request = self.create_review_request(submitter=self.user, publish=True)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'commit_id': commit_id}, expected_status=409)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], COMMIT_ID_ALREADY_EXISTS.code)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertIsNone(review_request.commit_id)
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    def test_put_with_commit_id_and_used_in_draft(self):
        """Testing the PUT review-requests/<id>/draft/ API with commit_id
        used in another review request draft
        """
        commit_id = b'abc123'
        existing_review_request = self.create_review_request(submitter=self.user, publish=True)
        existing_draft = ReviewRequestDraft.create(existing_review_request)
        existing_draft.commit_id = commit_id
        existing_draft.save(update_fields=('commit_id', ))
        review_request = self.create_review_request(submitter=self.user, publish=True)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'commit_id': commit_id}, expected_status=409)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], COMMIT_ID_ALREADY_EXISTS.code)
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertIsNone(review_request.commit_id)
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    def test_put_with_commit_id_empty_string(self):
        """Testing the PUT review-requests/<id>/draft/ API with commit_id=''"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'commit_id': b''}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIsNone(rsp[b'draft'][b'commit_id'])
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertIsNone(review_request.commit_id)
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    @add_fixtures([b'test_scmtools'])
    def test_put_with_commit_id_with_update_from_commit_id(self):
        """Testing the PUT review-requests/<id>/draft/ API with
        commit_id and update_from_commit_id=1
        """
        repository = self.create_repository(tool_name=b'Test')
        review_request = self.create_review_request(submitter=self.user, repository=repository, publish=True)
        ReviewRequestDraft.create(review_request)
        commit_id = b'abc123'
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'commit_id': commit_id, 
           b'update_from_commit_id': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'commit_id'], commit_id)
        self.assertEqual(rsp[b'draft'][b'summary'], b'Commit summary')
        self.assertEqual(rsp[b'draft'][b'description'], b'Commit description.')
        review_request = ReviewRequest.objects.get(pk=review_request.pk)
        self.assertNotEqual(review_request.commit_id, commit_id)
        self.assertNotEqual(review_request.description, b'Commit description.')
        self.assertNotEqual(review_request.summary, b'Commit summary')
        draft = review_request.get_draft()
        self.assertEqual(draft.commit_id, commit_id)
        self.assertEqual(draft.description, b'Commit description.')
        self.assertEqual(draft.summary, b'Commit summary')
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'commit_id', b'description', b'description_rich_text',
         b'diffset', b'last_updated', b'summary']))

    def test_put_with_depends_on(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with depends_on field
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        depends_1 = self.create_review_request(summary=b'Dependency 1', publish=True)
        depends_2 = self.create_review_request(summary=b'Dependency 2', publish=True)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'depends_on': b'%s, %s,,' % (depends_1.pk, depends_2.pk)}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        depends_on = rsp[b'draft'][b'depends_on']
        self.assertEqual(len(depends_on), 2)
        depends_on.sort(key=lambda x: x[b'title'])
        self.assertEqual(depends_on[0][b'title'], depends_1.summary)
        self.assertEqual(depends_on[1][b'title'], depends_2.summary)
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(list(draft.depends_on.order_by(b'pk')), [
         depends_1, depends_2])
        self.assertEqual(list(depends_1.draft_blocks.all()), [draft])
        self.assertEqual(list(depends_2.draft_blocks.all()), [draft])
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'last_updated']))

    @add_fixtures([b'test_site'])
    def test_put_with_depends_on_and_site(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with depends_on field and local site
        """
        review_request = self.create_review_request(submitter=b'doc', with_local_site=True)
        ReviewRequestDraft.create(review_request)
        self._login_user(local_site=True)
        depends_1 = self.create_review_request(with_local_site=True, submitter=self.user, summary=b'Test review request', local_id=3, publish=True)
        bad_depends = self.create_review_request(id=3, publish=True)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request, self.local_site_name), {b'depends_on': b'3'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        depends_on = rsp[b'draft'][b'depends_on']
        self.assertEqual(len(depends_on), 1)
        self.assertNotEqual(rsp[b'draft'][b'depends_on'][0][b'title'], bad_depends.summary)
        self.assertEqual(rsp[b'draft'][b'depends_on'][0][b'title'], depends_1.summary)
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(list(draft.depends_on.all()), [depends_1])
        self.assertEqual(list(depends_1.draft_blocks.all()), [draft])
        self.assertEqual(bad_depends.draft_blocks.count(), 0)
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'last_updated']))

    def test_put_with_depends_on_invalid_id(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with depends_on field and invalid ID
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'depends_on': b'10000,https://blah/,/r/123/,BUG-123'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'draft'][b'depends_on'], [])
        self.assertEqual(rsp[b'fields'], {b'depends_on': [
                         b'10000', b'https://blah/', b'/r/123/', b'BUG-123']})
        draft = review_request.get_draft()
        self.assertEqual(draft.depends_on.count(), 0)
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    @webapi_test_template
    def test_put_with_depends_on_and_emptying_list(self):
        """Testing the PUT <URL> API with depends_on emptying an existing
        list
        """
        dep1 = self.create_review_request(submitter=self.user, summary=b'Dep 1', publish=True)
        dep2 = self.create_review_request(submitter=self.user, summary=b'Dep 2', publish=True)
        self.create_review_request(submitter=self.user, summary=b'Dep 3', publish=True)
        review_request = self.create_review_request(submitter=self.user)
        draft = ReviewRequestDraft.create(review_request)
        draft.depends_on.add(dep1, dep2)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'depends_on': b''}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'depends_on'], [])
        draft = ReviewRequestDraft.objects.get(pk=draft.pk)
        self.assertEqual(draft.depends_on.count(), 0)
        return

    @webapi_test_template
    def test_put_with_summary(self):
        """Testing the PUT <URL> API with summary field"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'summary': b'New summary'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'summary'], b'New summary')
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(draft.summary, b'New summary')
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'last_updated', b'summary']))

    @webapi_test_template
    def test_put_with_summary_with_newline(self):
        """Testing the PUT <URL> API with summary field containing newline"""
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'summary': b'New summary\nbah'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'draft'][b'target_groups'], [])
        self.assertTrue(rsp[b'fields'], {b'summary': [
                      b"The summary can't contain a newline"]})
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(draft.summary, b'Test Summary')
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    @webapi_test_template
    def test_put_with_target_groups(self):
        """Testing the PUT <URL> API with target_groups field"""
        group1 = self.create_review_group(name=b'group1')
        group2 = self.create_review_group(name=b'group2')
        review_request = self.create_review_request(submitter=self.user, publish=True)
        ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'target_groups': b'group1,group2'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'target_groups'], [
         {b'href': b'http://testserver/api/groups/group1/', 
            b'method': b'GET', 
            b'title': b'group1'},
         {b'href': b'http://testserver/api/groups/group2/', 
            b'method': b'GET', 
            b'title': b'group2'}])
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(list(draft.target_groups.all()), [
         group1, group2])
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'last_updated']))

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_put_with_target_groups_with_local_site(self):
        """Testing the PUT <URL> API with target_groups field and Local Site
        draft
        """
        self.user = self._login_user(local_site=True)
        review_request = self.create_review_request(submitter=self.user, with_local_site=True, publish=True)
        ReviewRequestDraft.create(review_request)
        local_site = review_request.local_site
        group1 = self.create_review_group(name=b'group1', local_site=local_site)
        group2 = self.create_review_group(name=b'group2', local_site=local_site)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request, local_site), {b'target_groups': b'group1,group2'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'target_groups'], [
         {b'href': b'http://testserver/s/local-site-1/api/groups/group1/', 
            b'method': b'GET', 
            b'title': b'group1'},
         {b'href': b'http://testserver/s/local-site-1/api/groups/group2/', 
            b'method': b'GET', 
            b'title': b'group2'}])
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertEqual(list(draft.target_groups.all()), [
         group1, group2])
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'last_updated']))

    @add_fixtures([b'test_site'])
    @webapi_test_template
    def test_put_with_target_groups_with_local_site_and_global_group(self):
        """Testing the PUT <URL> API with target_groups field and Local Site
        draft with global group
        """
        self.user = self._login_user(local_site=True)
        review_request = self.create_review_request(submitter=self.user, with_local_site=True, publish=True)
        ReviewRequestDraft.create(review_request)
        local_site = review_request.local_site
        self.create_review_group(name=b'group1', local_site=local_site)
        self.create_review_group(name=b'group2')
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request, local_site), {b'target_groups': b'group1,group2'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'draft'][b'target_groups'], [])
        self.assertTrue(rsp[b'fields'], {b'target_groups': [
                            b'group2']})
        draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
        self.assertFalse(draft.target_groups.exists())
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)

    @webapi_test_template
    def test_put_with_target_groups_and_emptying_list(self):
        """Testing the PUT <URL> API with target_groups emptying an existing
        list
        """
        group1 = self.create_review_group(name=b'group1')
        group2 = self.create_review_group(name=b'group2')
        self.create_review_group(name=b'group3')
        review_request = self.create_review_request(submitter=self.user)
        draft = ReviewRequestDraft.create(review_request)
        draft.target_groups.add(group1, group2)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'target_groups': b''}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'target_groups'], [])
        draft = ReviewRequestDraft.objects.get(pk=draft.pk)
        self.assertEqual(draft.target_groups.count(), 0)
        return

    @webapi_test_template
    def test_put_with_target_people_and_emptying_list(self):
        """Testing the PUT <URL> API with target_people emptying an existing
        list
        """
        reviewer = User.objects.create(username=b'reviewer')
        review_request = self.create_review_request(submitter=self.user)
        draft = ReviewRequestDraft.create(review_request)
        draft.target_people.add(reviewer)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'target_people': b''}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'target_people'], [])
        draft = ReviewRequestDraft.objects.get(pk=draft.pk)
        self.assertEqual(draft.target_people.count(), 0)
        return

    @webapi_test_template
    def test_put_with_target_people_and_invalid_user(self):
        """Testing the PUT <URL> API with target_people containing invalid
        username
        """
        review_request = self.create_review_request(submitter=self.user)
        draft = ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'target_people': b'invalid'}, expected_status=INVALID_FORM_DATA.http_status)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'fields'], {b'target_people': [
                            b'invalid']})
        self.assertEqual(rsp[b'draft'][b'target_people'], [])
        draft = ReviewRequestDraft.objects.get(pk=draft.pk)
        self.assertFalse(draft.target_people.exists())
        self.assertFalse(ChangeDescription.save.called)
        self.assertFalse(ReviewRequestDraft.save.called)
        return

    @webapi_test_template
    def test_put_with_target_people_and_auth_backend_lookup(self):
        """Testing the PUT <URL> API with target_people and unknown user
        lookup in auth backend
        """

        def _get_or_create_user(*args, **kwargs):
            return User.objects.create(username=b'backend-user')

        review_request = self.create_review_request(submitter=self.user)
        draft = ReviewRequestDraft.create(review_request)
        self.spy_on(ChangeDescription.save, owner=ChangeDescription)
        self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
        self.spy_on(StandardAuthBackend.get_or_create_user, call_fake=_get_or_create_user)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'target_people': b'backend-user'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertEqual(rsp[b'draft'][b'target_people'], [
         {b'href': b'http://testserver/api/users/backend-user/', 
            b'method': b'GET', 
            b'title': b'backend-user'}])
        self.assertTrue(StandardAuthBackend.get_or_create_user.called_with(username=b'backend-user'))
        draft = ReviewRequestDraft.objects.get(pk=draft.pk)
        self.assertEqual(draft.target_people.count(), 1)
        self.assertEqual(draft.target_people.get().username, b'backend-user')
        self.assertFalse(ChangeDescription.save.called)
        self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=[
         b'last_updated']))
        return

    @webapi_test_template
    def test_put_with_target_people_and_auth_backend_lookup_error(self):
        """Testing the PUT <URL> API with target_people and unknown user
        lookup in auth backend errors
        """

        def _get_or_create_user(*args, **kwargs):
            raise Exception()

        self.spy_on(StandardAuthBackend.get_or_create_user, call_fake=_get_or_create_user)
        review_request = self.create_review_request(submitter=self.user)
        draft = ReviewRequestDraft.create(review_request)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'target_people': b'unknown'}, expected_status=INVALID_FORM_DATA.http_status)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertEqual(rsp[b'fields'], {b'target_people': [
                            b'unknown']})
        self.assertEqual(rsp[b'draft'][b'target_people'], [])
        self.assertTrue(StandardAuthBackend.get_or_create_user.called_with(username=b'unknown'))
        draft = ReviewRequestDraft.objects.get(pk=draft.pk)
        self.assertFalse(draft.target_people.exists())
        return

    def test_put_with_permission_denied_error(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with Permission Denied error
        """
        bugs_closed = b'123,456'
        review_request = self.create_review_request()
        self.assertNotEqual(review_request.submitter, self.user)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'bugs_closed': bugs_closed}, expected_status=403)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], PERMISSION_DENIED.code)

    def test_put_publish(self):
        """Testing the PUT review-requests/<id>/draft/?public=1 API"""
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            review_request = self.create_review_request(submitter=self.user, publish=True)
            draft = ReviewRequestDraft.create(review_request)
            draft.summary = b'My Summary'
            draft.description = b'My Description'
            draft.testing_done = b'My Testing Done'
            draft.branch = b'My Branch'
            draft.target_people.add(User.objects.get(username=b'doc'))
            draft.save()
            mail.outbox = []
            rsp = self.api_put(get_review_request_draft_url(review_request), {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertEqual(review_request.summary, b'My Summary')
        self.assertEqual(review_request.description, b'My Description')
        self.assertEqual(review_request.testing_done, b'My Testing Done')
        self.assertEqual(review_request.branch, b'My Branch')
        self.assertTrue(review_request.public)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, b'Re: Review Request %s: My Summary' % review_request.pk)
        self.assertValidRecipients([b'doc', b'grumpy'])

    def test_put_publish_with_new_submitter(self):
        """Testing the PUT review-requests/<id>/draft/?public=1 API
        with new submitter
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        draft = ReviewRequestDraft.create(review_request)
        draft.owner = User.objects.get(username=b'doc')
        draft.target_people = [draft.owner]
        draft.save()
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertEqual(review_request.submitter.username, b'doc')
        self.assertTrue(review_request.public)

    def test_put_publish_with_new_review_request(self):
        """Testing the PUT review-requests/<id>/draft/?public=1 API
        with a new review request
        """
        review_request = self.create_review_request(submitter=self.user)
        review_request.target_people = [
         User.objects.get(username=b'doc')]
        review_request.save()
        self._create_update_review_request(self.api_put, 200, review_request)
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            rsp = self.api_put(get_review_request_draft_url(review_request), {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertEqual(review_request.summary, b'My Summary')
        self.assertEqual(review_request.description, b'My Description')
        self.assertEqual(review_request.testing_done, b'My Testing Done')
        self.assertEqual(review_request.branch, b'My Branch')
        self.assertTrue(review_request.public)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, b'Review Request %s: My Summary' % review_request.pk)
        self.assertValidRecipients([b'doc', b'grumpy'], [])

    def test_put_as_other_user_with_permission(self):
        """Testing the PUT review-requests/<id>/draft/ API
        as another user with permission
        """
        self.user.user_permissions.add(Permission.objects.get(codename=b'can_edit_reviewrequest'))
        self._test_put_as_other_user()

    def test_put_as_other_user_with_admin(self):
        """Testing the PUT review-requests/<id>/draft/ API
        as another user with admin
        """
        self._login_user(admin=True)
        self._test_put_as_other_user()

    @add_fixtures([b'test_site'])
    def test_put_as_other_user_with_site_and_permission(self):
        """Testing the PUT review-requests/<id>/draft/ API
        as another user with local site and permission
        """
        self.user = self._login_user(local_site=True)
        local_site = self.get_local_site(name=self.local_site_name)
        site_profile = self.user.get_site_profile(local_site)
        site_profile.permissions[b'reviews.can_edit_reviewrequest'] = True
        site_profile.save(update_fields=('permissions', ))
        self._test_put_as_other_user(local_site)

    @add_fixtures([b'test_site'])
    def test_put_as_other_user_with_site_and_admin(self):
        """Testing the PUT review-requests/<id>/draft/ API
        as another user with local site and admin
        """
        self.user = self._login_user(local_site=True, admin=True)
        self._test_put_as_other_user(self.get_local_site(name=self.local_site_name))

    def test_put_with_invalid_submitter(self):
        """Testing the PUT review-requests/<id>/draft/ API with an invalid
        submitter
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'submitter': b'invalid'}, expected_status=INVALID_FORM_DATA.http_status)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], INVALID_FORM_DATA.code)
        self.assertTrue(b'submitter' in rsp[b'fields'])

    def test_put_with_publish_and_trivial(self):
        """Testing the PUT review-requests/<id>/draft/ API with trivial
        changes
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        draft = ReviewRequestDraft.create(review_request)
        draft.summary = b'My Summary'
        draft.description = b'My Description'
        draft.testing_done = b'My Testing Done'
        draft.branch = b'My Branch'
        draft.target_people.add(User.objects.get(username=b'doc'))
        draft.save()
        with self.siteconfig_settings({b'mail_send_review_mail': True}, reload_settings=False):
            rsp = self.api_put(get_review_request_draft_url(review_request), {b'public': True, 
               b'trivial': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertEqual(review_request.summary, b'My Summary')
        self.assertEqual(review_request.description, b'My Description')
        self.assertEqual(review_request.testing_done, b'My Testing Done')
        self.assertEqual(review_request.branch, b'My Branch')
        self.assertTrue(review_request.public)
        self.assertEqual(len(mail.outbox), 0)

    @add_fixtures([b'test_scmtools'])
    def test_put_with_publish_and_signal_handler_with_queries(self):
        """Testing the PUT review-requests/<id>/draft/?public=1 API with
        review_request_published signal handlers needing to fetch latest
        changedescs/diffsets
        """

        def _on_published(review_request, *args, **kwargs):
            self.assertEqual(len(review_request.changedescs.all()), expected_changedesc_count)
            self.assertEqual(len(review_request.diffset_history.diffsets.all()), expected_diffset_count)

        expected_changedesc_count = 0
        expected_diffset_count = 0
        review_request_published.connect(_on_published, weak=True)
        try:
            self.spy_on(_on_published)
            review_request = self.create_review_request(submitter=self.user, create_repository=True)
            draft_url = get_review_request_draft_url(review_request)
            draft = ReviewRequestDraft.create(review_request)
            draft.summary = b'My Summary'
            draft.description = b'My Description'
            draft.testing_done = b'My Testing Done'
            draft.branch = b'My Branch'
            draft.target_people.add(User.objects.get(username=b'doc'))
            draft.save()
            diffset = self.create_diffset(review_request, draft=True)
            self.create_filediff(diffset)
            self.assertEqual(len(review_request.changedescs.all()), expected_changedesc_count)
            self.assertEqual(len(review_request.diffset_history.diffsets.all()), expected_diffset_count)
            expected_diffset_count += 1
            rsp = self.api_put(draft_url, {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            self.assertTrue(_on_published.spy.called)
            _on_published.spy.reset_calls()
            diffset = self.create_diffset(review_request, draft=True)
            self.create_filediff(diffset)
            expected_changedesc_count += 1
            expected_diffset_count += 1
            rsp = self.api_put(draft_url, {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            self.assertTrue(_on_published.spy.called)
        finally:
            review_request_published.disconnect(_on_published)

    def test_put_with_publish_with_first_draft_as_other_user(self):
        """Testing the PUT review-requests/<id>/draft/ API with first draft
        as other user (with can_edit_reviewrequest after submit-as)
        """
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(self.user, user)
        self.user.user_permissions.add(Permission.objects.get(codename=b'can_edit_reviewrequest'))
        review_request = self.create_review_request(submitter=user, target_people=[
         user])
        ReviewRequestDraft.create(review_request)
        self.spy_on(review_request_publishing.send)
        self.spy_on(review_request_published.send)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'public': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertTrue(review_request.public)
        self.assertTrue(review_request_publishing.send.called_with(sender=ReviewRequest, user=user))
        self.assertTrue(review_request_published.send.called_with(sender=ReviewRequest, user=user))

    def test_put_with_publish_with_publish_as_owner(self):
        """Testing the PUT review-requests/<id>/draft/ API with
        publish_as_owner=
        """
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(self.user, user)
        self.user.user_permissions.add(Permission.objects.get(codename=b'can_edit_reviewrequest'))
        review_request = self.create_review_request(submitter=user, publish=True, target_people=[
         user])
        ReviewRequestDraft.create(review_request)
        self.spy_on(review_request_publishing.send)
        self.spy_on(review_request_published.send)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'summary': b'New summary', 
           b'public': True, 
           b'publish_as_owner': True}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_request = ReviewRequest.objects.get(pk=review_request.id)
        self.assertEqual(review_request.summary, b'New summary')
        self.assertTrue(review_request.public)
        self.assertTrue(review_request_publishing.send.called_with(sender=ReviewRequest, user=user))
        self.assertTrue(review_request_published.send.called_with(sender=ReviewRequest, user=user))

    def test_put_with_numeric_extra_data(self):
        """Testing the PUT review-requests/<id>/draft/ API with numeric
        extra_data values
        """
        review_request = self.create_review_request(submitter=self.user, publish=True)
        rsp = self.api_put(get_review_request_draft_url(review_request), {b'extra_data.int_val': 42, 
           b'extra_data.float_val': 3.14159, 
           b'extra_data.scientific_val': 2.75e-15}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        draft_rsp = rsp[b'draft']
        extra_data = draft_rsp[b'extra_data']
        self.assertEqual(extra_data[b'int_val'], 42)
        self.assertEqual(extra_data[b'float_val'], 3.14159)
        self.assertEqual(extra_data[b'scientific_val'], 2.75e-15)

    def test_get_or_create_user_auth_backend(self):
        """Testing the PUT review-requests/<id>/draft/ API
        with AuthBackend.get_or_create_user failure
        """

        class SandboxAuthBackend(AuthBackend):
            backend_id = b'test-id'
            name = b'test'

            def get_or_create_user(self, username, request=None, password=None):
                raise Exception

        backend = SandboxAuthBackend()
        self.spy_on(auth.get_backends, call_fake=lambda : [backend])
        self.spy_on(ReviewRequest.is_mutable_by, call_fake=lambda x, y: True)
        self.spy_on(backend.get_or_create_user)
        review_request = self.create_review_request(submitter=self.user)
        ReviewRequestDraft.create(review_request)
        rsp = self.api_put(get_review_request_draft_url(review_request, None), {b'target_people': b'Target'}, expected_status=400)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertTrue(backend.get_or_create_user.called)
        return

    def _create_update_review_request(self, api_func, expected_status, review_request=None, local_site_name=None):
        summary = b'My Summary'
        description = b'My Description'
        testing_done = b'My Testing Done'
        branch = b'My Branch'
        bugs = b'#123,456'
        if review_request is None:
            review_request = self.create_review_request(submitter=self.user, publish=True)
            review_request.target_people.add(User.objects.get(username=b'doc'))
        func_kwargs = {b'summary': summary, 
           b'description': description, 
           b'testing_done': testing_done, 
           b'branch': branch, 
           b'bugs_closed': bugs}
        if expected_status >= 400:
            expected_mimetype = None
        else:
            expected_mimetype = review_request_draft_item_mimetype
        rsp = api_func(get_review_request_draft_url(review_request, local_site_name), func_kwargs, expected_status=expected_status, expected_mimetype=expected_mimetype)
        if expected_status >= 200 and expected_status < 300:
            self.assertEqual(rsp[b'stat'], b'ok')
            self.assertEqual(rsp[b'draft'][b'summary'], summary)
            self.assertEqual(rsp[b'draft'][b'description'], description)
            self.assertEqual(rsp[b'draft'][b'testing_done'], testing_done)
            self.assertEqual(rsp[b'draft'][b'branch'], branch)
            self.assertEqual(rsp[b'draft'][b'bugs_closed'], [b'123', b'456'])
            draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
            self.assertEqual(draft.summary, summary)
            self.assertEqual(draft.description, description)
            self.assertEqual(draft.testing_done, testing_done)
            self.assertEqual(draft.branch, branch)
            self.assertEqual(draft.get_bug_list(), [b'123', b'456'])
        return rsp

    def _create_update_review_request_with_site(self, api_func, expected_status, relogin=True, review_request=None):
        if relogin:
            self._login_user(local_site=True)
        if review_request is None:
            review_request = self.create_review_request(submitter=b'doc', with_local_site=True)
        return self._create_update_review_request(api_func, expected_status, review_request, self.local_site_name)

    def _test_get_with_force_text_type(self, text, rich_text, force_text_type, expected_text):
        url, mimetype, draft = self.setup_basic_get_test(self.user, False, None)
        draft.description = text
        draft.testing_done = text
        draft.description_rich_text = rich_text
        draft.testing_done_rich_text = rich_text
        draft.save()
        draft.changedesc.text = text
        draft.changedesc.rich_text = rich_text
        draft.changedesc.save()
        rsp = self.api_get(url + b'?force-text-type=%s' % force_text_type, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        draft_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(draft_rsp[b'description_text_type'], force_text_type)
        self.assertEqual(draft_rsp[b'testing_done_text_type'], force_text_type)
        self.assertEqual(draft_rsp[b'changedescription'], expected_text)
        self.assertEqual(draft_rsp[b'description'], expected_text)
        self.assertEqual(draft_rsp[b'testing_done'], expected_text)
        self.assertNotIn(b'raw_text_fields', draft_rsp)
        rsp = self.api_get(b'%s?force-text-type=%s&include-text-types=raw' % (
         url, force_text_type), expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        draft_rsp = rsp[self.resource.item_result_key]
        self.assertIn(b'raw_text_fields', draft_rsp)
        raw_text_fields = draft_rsp[b'raw_text_fields']
        self.assertEqual(raw_text_fields[b'changedescription'], text)
        self.assertEqual(raw_text_fields[b'description'], text)
        self.assertEqual(raw_text_fields[b'testing_done'], text)
        return

    def _test_get_with_custom_and_force(self, source_text, rich_text, force_text_type, expected_text, custom_field_supports_markdown):
        """Helper function to test custom fields and ``?include-text-types=``.

        This will test GET requests of custom text fields in two alternative
        formats (one fixed as ``raw`` and the other controlled by
        ``force_text_type``) via the ``?include-text-types=`` query parameter.

        Args:
            source_text (unicode):
                Text to use as source data for fields being tested.

            rich_text (bool):
                Whether ``source_text`` is rich text.

            force_text_type (unicode):
                Value for ``?force-text-type=`` query parameter. Should be one
                of: ``plain``, ``markdown`` or ``html``.

            expected_text (unicode):
                Expected resultant text after forcing ``source_text`` to
                requested format.

            custom_field_supports_markdown (bool)
                Whether custom field being tested should enable markdown
                support.
        """
        if custom_field_supports_markdown:
            base = BaseTextAreaField
        else:
            base = BaseEditableField

        class CustomField(base):
            field_id = b'text'

        fieldset = get_review_request_fieldset(b'main')
        fieldset.add_field(CustomField)
        try:
            url, mimetype, draft = self.setup_basic_get_test(self.user, False, None)
            source_text_type = b'markdown' if rich_text else b'plain'
            draft.description = source_text
            draft.description_rich_text = rich_text
            draft.extra_data[b'text'] = source_text
            if custom_field_supports_markdown:
                draft.extra_data[b'text_type'] = source_text_type
            draft.save()
            rsp = self.api_get(url + b'?force-text-type=%s' % force_text_type, expected_mimetype=mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            self.assertIn(self.resource.item_result_key, rsp)
            draft_rsp = rsp[self.resource.item_result_key]
            self.assertIn(b'extra_data', draft_rsp)
            extra_data = draft_rsp[b'extra_data']
            self.assertEqual(draft_rsp[b'description_text_type'], force_text_type)
            self.assertEqual(draft_rsp[b'description'], expected_text)
            self.assertNotIn(b'raw_text_fields', draft_rsp)
            if custom_field_supports_markdown:
                self.assertNotIn(b'text_text_type', extra_data)
                self.assertEqual(extra_data[b'text'], expected_text)
                self.assertEqual(extra_data[b'text_type'], force_text_type)
            else:
                self.assertEqual(extra_data[b'text'], source_text)
                self.assertNotIn(b'text_type', extra_data)
            rsp = self.api_get(b'%s?force-text-type=%s&include-text-types=raw,%s' % (
             url, force_text_type, force_text_type), expected_mimetype=mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            draft_rsp = rsp[self.resource.item_result_key]
            self.assertIn(b'raw_text_fields', draft_rsp)
            raw_text_fields = draft_rsp[b'raw_text_fields']
            self.assertEqual(raw_text_fields[b'description'], source_text)
            self.assertEqual(raw_text_fields[b'description_text_type'], source_text_type)
            other_field_name = b'%s_text_fields' % force_text_type
            self.assertIn(other_field_name, draft_rsp)
            other_text_fields = draft_rsp[other_field_name]
            self.assertEqual(other_text_fields[b'description'], expected_text)
            self.assertEqual(other_text_fields[b'description_text_type'], force_text_type)
            if custom_field_supports_markdown:
                self.assertIn(b'extra_data', raw_text_fields)
                extra_data_raw = raw_text_fields[b'extra_data']
                self.assertEqual(extra_data_raw[b'text'], source_text)
                self.assertEqual(extra_data_raw[b'text_type'], source_text_type)
                self.assertIn(b'extra_data', other_text_fields)
                extra_data_other = other_text_fields[b'extra_data']
                self.assertEqual(extra_data_other[b'text'], expected_text)
                self.assertEqual(extra_data_other[b'text_type'], force_text_type)
            else:
                self.assertNotIn(b'extra_data', raw_text_fields)
                self.assertNotIn(b'extra_data', other_text_fields)
        finally:
            fieldset.remove_field(CustomField)

        return

    def _test_put_with_text_types(self, text_type_field, text_type_value, expected_change_text_type, expected_description_text_type, expected_testing_done_text_type, expected_custom_field_text_type, expected_changedesc_update_fields=[], expected_draft_update_fields=[]):
        text = b'`This` is a **test**'

        class CustomField(BaseTextAreaField):
            field_id = b'mytext'

        fieldset = get_review_request_fieldset(b'main')
        fieldset.add_field(CustomField)
        try:
            review_request = self.create_review_request(submitter=self.user, publish=True)
            ReviewRequestDraft.create(review_request)
            self.spy_on(ChangeDescription.save, owner=ChangeDescription)
            self.spy_on(ReviewRequestDraft.save, owner=ReviewRequestDraft)
            rsp = self.api_put(get_review_request_draft_url(review_request), {b'changedescription': text, 
               b'description': text, 
               b'testing_done': text, 
               b'extra_data.mytext': text, 
               text_type_field: text_type_value}, expected_mimetype=review_request_draft_item_mimetype)
            self.assertEqual(rsp[b'stat'], b'ok')
            draft_rsp = rsp[b'draft']
            extra_data = draft_rsp[b'extra_data']
            self.assertEqual(draft_rsp[b'changedescription'], text)
            self.assertEqual(draft_rsp[b'description'], text)
            self.assertEqual(draft_rsp[b'testing_done'], text)
            self.assertEqual(extra_data[b'mytext'], text)
            self.assertEqual(draft_rsp[b'changedescription_text_type'], expected_change_text_type)
            self.assertEqual(draft_rsp[b'description_text_type'], expected_description_text_type)
            self.assertEqual(draft_rsp[b'testing_done_text_type'], expected_testing_done_text_type)
            self.assertEqual(extra_data[b'mytext_text_type'], expected_custom_field_text_type)
            draft = ReviewRequestDraft.objects.get(pk=rsp[b'draft'][b'id'])
            self.compare_item(draft_rsp, draft)
            self.assertTrue(ChangeDescription.save.last_called_with(update_fields=sorted([b'text'] + expected_changedesc_update_fields)))
            self.assertTrue(ReviewRequestDraft.save.last_called_with(update_fields=sorted([b'description', b'extra_data',
             b'last_updated', b'testing_done'] + expected_draft_update_fields)))
        finally:
            fieldset.remove_field(CustomField)

    def _test_put_as_other_user(self, local_site=None):
        review_request = self.create_review_request(with_local_site=local_site is not None, submitter=b'dopey', publish=True)
        self.assertNotEqual(review_request.submitter, self.user)
        ReviewRequestDraft.create(review_request)
        if local_site:
            local_site_name = local_site.name
        else:
            local_site_name = None
        rsp = self.api_put(get_review_request_draft_url(review_request, local_site_name), {b'description': b'New description'}, expected_mimetype=review_request_draft_item_mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertTrue(rsp[b'draft'][b'description'], b'New description')
        return