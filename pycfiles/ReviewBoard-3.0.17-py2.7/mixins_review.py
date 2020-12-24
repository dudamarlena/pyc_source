# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/webapi/tests/mixins_review.py
# Compiled at: 2020-02-11 04:03:57
from __future__ import unicode_literals
from djblets.webapi.testing.decorators import webapi_test_template
from reviewboard.webapi.tests.mixins_extra_data import ExtraDataItemMixin, ExtraDataListMixin

class ReviewListMixin(ExtraDataListMixin):

    @webapi_test_template
    def test_post_with_text_type_markdown(self):
        """Testing the POST <URL> API with text_type=markdown"""
        self._test_post_with_text_types(text_type_field=b'text_type', text_type_value=b'markdown', expected_body_top_text_type=b'markdown', expected_body_bottom_text_type=b'markdown')

    @webapi_test_template
    def test_post_with_text_type_plain(self):
        """Testing the POST <URL> API with text_type=plain"""
        self._test_post_with_text_types(text_type_field=b'text_type', text_type_value=b'plain', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'plain')

    @webapi_test_template
    def test_post_with_body_top_text_type_markdown(self):
        """Testing the POST <URL> API with body_top_text_type=markdown"""
        self._test_post_with_text_types(text_type_field=b'body_top_text_type', text_type_value=b'markdown', expected_body_top_text_type=b'markdown', expected_body_bottom_text_type=b'plain')

    @webapi_test_template
    def test_post_with_body_top_text_type_plain(self):
        """Testing the POST <URL> API with body_top_text_type=plain"""
        self._test_post_with_text_types(text_type_field=b'body_top_text_type', text_type_value=b'plain', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'plain')

    @webapi_test_template
    def test_post_with_body_bottom_text_type_markdown(self):
        """Testing the POST <URL> API with body_bottom_text_type=markdown"""
        self._test_post_with_text_types(text_type_field=b'body_bottom_text_type', text_type_value=b'markdown', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'markdown')

    @webapi_test_template
    def test_post_with_body_bottom_text_type_plain(self):
        """Testing the POST <URL> API with body_bottom_text_type=plain"""
        self._test_post_with_text_types(text_type_field=b'body_bottom_text_type', text_type_value=b'plain', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'plain')

    def _test_post_with_text_types(self, text_type_field, text_type_value, expected_body_top_text_type, expected_body_bottom_text_type):
        body_top = b'`This` is **body_top**'
        body_bottom = b'`This` is **body_bottom**'
        url, mimetype, data, objs = self.setup_basic_post_test(self.user, False, None, True)
        rsp = self.api_post(url, {b'body_top': body_top, 
           b'body_bottom': body_bottom, 
           text_type_field: text_type_value}, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(review_rsp[b'body_top'], body_top)
        self.assertEqual(review_rsp[b'body_bottom'], body_bottom)
        self.assertEqual(review_rsp[b'body_top_text_type'], expected_body_top_text_type)
        self.assertEqual(review_rsp[b'body_bottom_text_type'], expected_body_bottom_text_type)
        self.compare_item(review_rsp, self.resource.model.objects.get(pk=review_rsp[b'id']))
        return


class ReviewItemMixin(ExtraDataItemMixin):

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
    def test_put_with_text_type_markdown(self):
        """Testing the PUT <URL> API with text_type=markdown"""
        self._test_put_with_text_types(text_type_field=b'text_type', text_type_value=b'markdown', expected_body_top_text_type=b'markdown', expected_body_bottom_text_type=b'markdown')

    @webapi_test_template
    def test_put_with_text_type_plain(self):
        """Testing the PUT <URL> API with text_type=plain"""
        self._test_put_with_text_types(text_type_field=b'text_type', text_type_value=b'plain', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'plain')

    @webapi_test_template
    def test_put_with_body_top_text_type_markdown(self):
        """Testing the PUT <URL> API with body_top_text_type=markdown"""
        self._test_put_with_text_types(text_type_field=b'body_top_text_type', text_type_value=b'markdown', expected_body_top_text_type=b'markdown', expected_body_bottom_text_type=b'plain')

    @webapi_test_template
    def test_put_with_body_top_text_type_plain(self):
        """Testing the PUT <URL> API with body_top_text_type=plain"""
        self._test_put_with_text_types(text_type_field=b'body_top_text_type', text_type_value=b'plain', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'plain')

    @webapi_test_template
    def test_put_with_body_bottom_text_type_markdown(self):
        """Testing the PUT <URL> API with body_bottom_text_type=markdown"""
        self._test_put_with_text_types(text_type_field=b'body_bottom_text_type', text_type_value=b'markdown', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'markdown')

    @webapi_test_template
    def test_put_with_body_bottom_text_type_plain(self):
        """Testing the PUT <URL> API with body_bottom_text_type=plain"""
        self._test_put_with_text_types(text_type_field=b'body_bottom_text_type', text_type_value=b'plain', expected_body_top_text_type=b'plain', expected_body_bottom_text_type=b'plain')

    def _test_get_with_force_text_type(self, text, rich_text, force_text_type, expected_text):
        url, mimetype, review = self.setup_basic_get_test(self.user, False, None)
        review.body_top = text
        review.body_bottom = text
        review.body_top_rich_text = rich_text
        review.body_bottom_rich_text = rich_text
        review.save()
        rsp = self.api_get(url + b'?force-text-type=%s' % force_text_type, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        self.assertIn(self.resource.item_result_key, rsp)
        review_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(review_rsp[b'body_top_text_type'], force_text_type)
        self.assertEqual(review_rsp[b'body_bottom_text_type'], force_text_type)
        self.assertEqual(review_rsp[b'body_top'], expected_text)
        self.assertEqual(review_rsp[b'body_bottom'], expected_text)
        self.assertNotIn(b'raw_text_fields', review_rsp)
        rsp = self.api_get(b'%s?force-text-type=%s&include-text-types=raw' % (
         url, force_text_type), expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_rsp = rsp[self.resource.item_result_key]
        self.assertIn(b'raw_text_fields', review_rsp)
        raw_text_fields = review_rsp[b'raw_text_fields']
        self.assertEqual(raw_text_fields[b'body_top'], text)
        self.assertEqual(raw_text_fields[b'body_bottom'], text)
        return

    def _test_put_with_text_types(self, text_type_field, text_type_value, expected_body_top_text_type, expected_body_bottom_text_type):
        body_top = b'`This` is **body_top**'
        body_bottom = b'`This` is **body_bottom**'
        url, mimetype, data, review, objs = self.setup_basic_put_test(self.user, False, None, True)
        data.update({b'body_top': body_top, 
           b'body_bottom': body_bottom, 
           text_type_field: text_type_value})
        rsp = self.api_put(url, data, expected_mimetype=mimetype)
        self.assertEqual(rsp[b'stat'], b'ok')
        review_rsp = rsp[self.resource.item_result_key]
        self.assertEqual(review_rsp[b'body_top'], body_top)
        self.assertEqual(review_rsp[b'body_bottom'], body_bottom)
        self.assertEqual(review_rsp[b'body_top_text_type'], expected_body_top_text_type)
        self.assertEqual(review_rsp[b'body_bottom_text_type'], expected_body_bottom_text_type)
        self.compare_item(review_rsp, self.resource.model.objects.get(pk=review_rsp[b'id']))
        return