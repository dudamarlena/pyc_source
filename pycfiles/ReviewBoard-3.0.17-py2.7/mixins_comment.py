# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/mixins_comment.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from django.contrib.auth.models import User
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin

class BaseCommentListMixin(object):

    @webapi_test_template
    def test_post_with_text_type_markdown(self):
        """Testing the POST <URL> API with text_type=markdown"""
        self._test_post_with_text_type(b'markdown')

    @webapi_test_template
    def test_post_with_text_type_plain(self):
        """Testing the POST <URL> API with text_type=plain"""
        self._test_post_with_text_type(b'plain')

    def _test_post_with_text_type(self, text_type):
        comment_text = b'`This` is a **test**'
        url, mimetype, data, objs = self.setup_basic_post_test(self.user, False, None, True)
        data[b'text'] = comment_text
        data[b'text_type'] = text_type
        rsp = self.api_post(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        comment_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(comment_rsp[b'text'], comment_text)
        self.assertEqual(comment_rsp[b'text_type'], text_type)
        comment = self.resource.model.objects.get(pk=comment_rsp[b'id'])
        self.compare_item(comment_rsp, comment)
        return


class BaseCommentItemMixin(object):

    def compare_item(self, item_rsp, comment):
        self.assertEqual(item_rsp[b'id'], comment.pk)
        self.assertEqual(item_rsp[b'text'], comment.text)
        if comment.rich_text:
            self.assertEqual(item_rsp[b'rich_text'], b'markdown')
        else:
            self.assertEqual(item_rsp[b'rich_text'], b'plain')

    @webapi_test_template
    def test_get_with_markdown_and_force_text_type_markdown(self):
        """Testing the GET <URL> API with text_type=markdown and
        ?force-text-type=markdown
        """
        self._test_get_with_force_text_type(text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'markdown', expected_text=b'\\# `This` is a **test**')

    @webapi_test_template
    def test_get_with_markdown_and_force_text_type_plain(self):
        """Testing the GET <URL> API with text_type=markdown and
        ?force-text-type=plain
        """
        self._test_get_with_force_text_type(text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'plain', expected_text=b'# `This` is a **test**')

    @webapi_test_template
    def test_get_with_markdown_and_force_text_type_html(self):
        """Testing the GET <URL> API with text_type=markdown and
        ?force-text-type=html
        """
        self._test_get_with_force_text_type(text=b'\\# `This` is a **test**', rich_text=True, force_text_type=b'html', expected_text=b'<p># <code>This</code> is a <strong>test</strong></p>')

    @webapi_test_template
    def test_get_with_plain_and_force_text_type_markdown(self):
        """Testing the GET <URL> API with text_type=plain and
        ?force-text-type=markdown
        """
        self._test_get_with_force_text_type(text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'markdown', expected_text=b'\\#<\\`This\\` is a \\*\\*test\\*\\*>')

    @webapi_test_template
    def test_get_with_plain_and_force_text_type_plain(self):
        """Testing the GET <URL> API with text_type=plain and
        ?force-text-type=plain
        """
        self._test_get_with_force_text_type(text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'plain', expected_text=b'#<`This` is a **test**>')

    @webapi_test_template
    def test_get_with_plain_and_force_text_type_html(self):
        """Testing the GET <URL> API with text_type=plain and
        ?force-text-type=html
        """
        self._test_get_with_force_text_type(text=b'#<`This` is a **test**>', rich_text=False, force_text_type=b'html', expected_text=b'#&lt;`This` is a **test**&gt;')

    @webapi_test_template
    def test_put_with_text_type_markdown_and_text(self):
        """Testing the PUT <URL> API
        with text_type=markdown and text specified
        """
        self._test_put_with_text_type_and_text(b'markdown')

    @webapi_test_template
    def test_put_with_text_type_plain_and_text(self):
        """Testing the PUT <URL> API with text_type=plain and text specified"""
        self._test_put_with_text_type_and_text(b'plain')

    @webapi_test_template
    def test_put_with_text_type_markdown_and_not_text(self):
        """Testing the PUT <URL> API
        with text_type=markdown and text not specified escapes text
        """
        self._test_put_with_text_type_and_not_text(b'markdown', b'`Test` **diff** comment', b'\\`Test\\` \\*\\*diff\\*\\* comment')

    @webapi_test_template
    def test_put_with_text_type_plain_and_not_text(self):
        """Testing the PUT <URL> API
        with text_type=plain and text not specified
        """
        self._test_put_with_text_type_and_not_text(b'plain', b'\\`Test\\` \\*\\*diff\\*\\* comment', b'`Test` **diff** comment')

    @webapi_test_template
    def test_put_without_text_type_and_escaping_provided_fields(self):
        """Testing the PUT <URL> API
        without changing text_type and with escaping provided fields
        """
        url, mimetype, data, reply_comment, objs = self.setup_basic_put_test(self.user, False, None, True)
        reply_comment.rich_text = True
        reply_comment.save()
        if b'text_type' in data:
            del data[b'text_type']
        data.update({b'text': b'`This` is **text**'})
        rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        comment_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(comment_rsp[b'text_type'], b'markdown')
        self.assertEqual(comment_rsp[b'text'], b'\\`This\\` is \\*\\*text\\*\\*')
        comment = self.resource.model.objects.get(pk=comment_rsp[b'id'])
        self.compare_item(comment_rsp, comment)
        return

    @webapi_test_template
    def test_put_with_multiple_include_text_types(self):
        """Testing the PUT <URL> API with multiple include-text-types"""
        url, mimetype, data, reply_comment, objs = self.setup_basic_put_test(self.user, False, None, True)
        data.update({b'include_text_types': b'raw,plain,markdown,html', 
           b'text': b'Foo'})
        rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        return

    @webapi_test_template
    def test_put_with_issue_verification_success(self):
        """Testing the PUT <URL> API with issue verification success"""
        url, mimetype, data, comment, objs = self.setup_basic_put_test(self.user, False, None, True)
        comment.require_verification = True
        comment.save()
        rsp = self.api_put(url, {b'issue_status': b'resolved'}, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        return

    @webapi_test_template
    def test_put_with_issue_verification_permission_denied(self):
        """Testing the PUT <URL> API with issue verification permission denied
        """
        user = User.objects.get(username=b'doc')
        self.assertNotEqual(user, self.user)
        url, mimetype, data, comment, objs = self.setup_basic_put_test(user, False, None, True)
        comment.require_verification = True
        comment.save()
        rsp = self.api_put(url, {b'issue_status': b'resolved'}, expected_status=self.not_owner_status_code)
        self.assertEqual(rsp[b'stat'], b'fail')
        self.assertEqual(rsp[b'err'][b'code'], self.not_owner_error.code)
        return

    def _test_get_with_force_text_type(self, text, rich_text, force_text_type, expected_text):
        url, mimetype, comment = self.setup_basic_get_test(self.user, False, None)
        comment.text = text
        comment.rich_text = rich_text
        comment.save()
        rsp = self.api_get(url + b'?force-text-type=%s' % force_text_type, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        comment_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(comment_rsp[b'text_type'], force_text_type)
        self.assertEqual(comment_rsp[b'text'], expected_text)
        self.assertNotIn(b'raw_text_fields', comment_rsp)
        rsp = self.api_get(b'%s?force-text-type=%s&include-text-types=raw' % (
         url, force_text_type), expected_mimetype=mimetype)
        comment_rsp = rsp[self.resource.item_result_key]
        self.assertIn(b'raw_text_fields', comment_rsp)
        self.assertEqual(comment_rsp[b'raw_text_fields'][b'text'], text)
        return

    def _test_put_with_text_type_and_text(self, text_type):
        comment_text = b'`Test` **diff** comment'
        url, mimetype, data, reply_comment, objs = self.setup_basic_put_test(self.user, False, None, True)
        data[b'text_type'] = text_type
        data[b'text'] = comment_text
        rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        comment_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(comment_rsp[b'text'], comment_text)
        self.assertEqual(comment_rsp[b'text_type'], text_type)
        comment = self.resource.model.objects.get(pk=comment_rsp[b'id'])
        self.compare_item(comment_rsp, comment)
        return

    def _test_put_with_text_type_and_not_text(self, text_type, text, expected_text):
        self.assertIn(text_type, ('markdown', 'plain'))
        rich_text = text_type == b'markdown'
        url, mimetype, data, reply_comment, objs = self.setup_basic_put_test(self.user, False, None, True)
        reply_comment.text = text
        reply_comment.rich_text = not rich_text
        reply_comment.save()
        data[b'text_type'] = text_type
        if b'text' in data:
            del data[b'text']
        rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        comment_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(comment_rsp[b'text'], expected_text)
        self.assertEqual(comment_rsp[b'text_type'], text_type)
        comment = self.resource.model.objects.get(pk=comment_rsp[b'id'])
        self.compare_item(comment_rsp, comment)
        return


class CommentListMixin(ExtraDataListMixin, BaseCommentListMixin):
    pass


class CommentItemMixin(ExtraDataItemMixin, BaseCommentItemMixin):
    pass


class CommentReplyListMixin(BaseCommentListMixin):
    pass


class CommentReplyItemMixin(BaseCommentItemMixin):
    pass