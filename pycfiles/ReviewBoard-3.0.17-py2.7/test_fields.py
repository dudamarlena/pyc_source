# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_fields.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.utils import six
from djblets.testing.decorators import add_fixtures
from reviewboard.reviews.fields import BaseTextAreaField
from reviewboard.reviews.models import ReviewRequest
from reviewboard.testing import TestCase

class BaseTextAreaFieldTests(TestCase):
    """Unit tests for reviewboard.reviews.fields.BaseTextAreaField."""

    def test_render_change_entry_html(self):
        """Testing BaseTextAreaField.render_change_entry_html"""
        field = BaseTextAreaField(ReviewRequest())
        html = field.render_change_entry_html({b'old': [
                  b'This is a test\n\nWith two lines'], 
           b'new': [
                  b'This is a test with one line']})
        self.assertHTMLEqual(html, b'<table class="diffed-text-area"> <tr class="replace-old">  <td class="marker">~</td>  <td class="marker">&nbsp;</td>  <td class="line rich-text"><p>This is a test</p></td> </tr> <tr class="replace-new">  <td class="marker">&nbsp;</td>  <td class="marker">~</td>  <td class="line rich-text">   <p>This is a test<span class="hl"> with one line</span></p>  </td> </tr> <tr class="delete">  <td class="marker">-</td>  <td class="marker">&nbsp;</td>  <td class="line rich-text">\n</td> </tr> <tr class="delete">  <td class="marker">-</td>  <td class="marker">&nbsp;</td>  <td class="line rich-text"><p>With two lines</p></td> </tr></table>')

    def test_render_change_entry_html_with_entities(self):
        """Testing BaseTextAreaField.render_change_entry_html with string
        containing entities
        """
        field = BaseTextAreaField(ReviewRequest())
        html = field.render_change_entry_html({b'old': [
                  b'This "is" a <test>'], 
           b'new': [
                  b'This "is" a <test> with more stuff here']})
        self.assertHTMLEqual(html, b'<table class="diffed-text-area"> <tr class="replace-old">  <td class="marker">~</td>  <td class="marker">&nbsp;</td>  <td class="line rich-text">   <p>This &quot;is&quot; a &lt;test&gt;</p>  </td> </tr> <tr class="replace-new">  <td class="marker">&nbsp;</td>  <td class="marker">~</td>  <td class="line rich-text">   <p>This &quot;is&quot; a &lt;test&gt;<span class="hl"> with       more stuff here</span></p>  </td> </tr></table>')


class FieldTests(TestCase):
    """Unit tests for review request fields."""

    def test_long_bug_numbers(self):
        """Testing review requests with very long bug numbers"""
        review_request = ReviewRequest()
        review_request.bugs_closed = b'12006153200030304432010,4432009'
        self.assertEqual(review_request.get_bug_list(), [
         b'4432009', b'12006153200030304432010'])

    def test_no_summary(self):
        """Testing review requests with no summary"""
        from django.template.defaultfilters import lower
        review_request = ReviewRequest()
        lower(review_request)

    @add_fixtures([b'test_users'])
    def test_commit_id(self):
        """Testing commit_id migration"""
        review_request = self.create_review_request()
        review_request.changenum = b'123'
        self.assertEqual(review_request.commit_id, None)
        self.assertEqual(review_request.commit, six.text_type(review_request.changenum))
        self.assertNotEqual(review_request.commit_id, None)
        return