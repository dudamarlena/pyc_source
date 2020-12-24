# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/rbcommenttype/extension.py
# Compiled at: 2015-12-14 18:14:24
from __future__ import unicode_literals
import json
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from reviewboard.extensions.base import Extension, JSExtension
from reviewboard.extensions.hooks import CommentDetailDisplayHook, TemplateHook
from reviewboard.urls import reviewable_url_names, review_request_url_names
apply_to_url_names = set(reviewable_url_names + review_request_url_names)

class CommentTypeCommentDetailDisplay(CommentDetailDisplayHook):
    """Adds detect type information to displayed comments."""

    def render_review_comment_detail(self, comment):
        """Render the comment type to HTML."""
        comment_type = comment.extra_data.get(b'commentType')
        if not comment_type:
            return b''
        return format_html(b'<p class="comment-type"><label>{0}</label> {1}</p>', _(b'Type:'), comment_type)


class CommentTypeJSExtension(JSExtension):
    """JavaScript extension for comment types."""
    model_class = b'RBCommentType.Extension'
    apply_to = apply_to_url_names


class CommentTypeExtension(Extension):
    """Extends Review Board with comment comment categorization.

    When creating or updating comments, users will be allowed to choose a
    category for the comment. These categories can be configured in the
    extension settings, and can be fetched from the comment's ``extra_data``
    field.
    """
    metadata = {b'Name': b'Comment Categorization'}
    is_configurable = True
    js_extensions = [
     CommentTypeJSExtension]
    css_bundles = {b'comment-type-configure': {b'source_filenames': [
                                                       b'css/configure.less'], 
                                   b'apply_to': b'rbcommenttype-configure'}}
    js_bundles = {b'comment-type': {b'source_filenames': [
                                             b'js/commentType.js'], 
                         b'apply_to': apply_to_url_names}, 
       b'comment-type-configure': {b'source_filenames': [
                                                       b'js/configure.js'], 
                                   b'apply_to': b'rbcommenttype-configure'}}

    def initialize(self):
        """Initialize the extension."""
        CommentTypeCommentDetailDisplay(self)
        TemplateHook(self, b'base-scripts-post', b'rbcommenttype-types.html', apply_to=apply_to_url_names)

    @property
    def configured_types(self):
        """Return a list of the configured type names."""
        types = [ t[b'type'] for t in self.settings.get(b'types', []) if t[b'visible']
                ]
        if not self.settings.get(b'require_type', False):
            types.insert(0, b'')
        return json.dumps(types)