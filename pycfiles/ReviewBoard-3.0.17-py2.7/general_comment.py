# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/models/general_comment.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.reviews.models.base_comment import BaseComment
from django.utils.translation import ugettext_lazy as _

class GeneralComment(BaseComment):
    """A comment on a review request that is not tied to any code or file.

    A general comment on a review request is used when a comment is not tied
    to specific lines of code or a special file attachment, and an issue is
    opened. Examples include suggestions for testing or pointing out errors
    in the change description.
    """
    anchor_prefix = b'gcomment'
    comment_type = b'general'

    def get_absolute_url(self):
        return self.get_review_url()

    class Meta:
        app_label = b'reviews'
        db_table = b'reviews_generalcomment'
        verbose_name = _(b'General Comment')
        verbose_name_plural = _(b'General Comments')