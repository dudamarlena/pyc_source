# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/models/diff_comment.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.db import models
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from reviewboard.diffviewer.models import FileDiff
from reviewboard.reviews.models.base_comment import BaseComment

class Comment(BaseComment):
    """A comment made on a diff.

    A comment can belong to a single filediff or to an interdiff between
    two filediffs. It can also have multiple replies.
    """
    anchor_prefix = b'comment'
    comment_type = b'diff'
    filediff = models.ForeignKey(FileDiff, verbose_name=_(b'file diff'), related_name=b'comments')
    interfilediff = models.ForeignKey(FileDiff, verbose_name=_(b'interdiff file'), blank=True, null=True, related_name=b'interdiff_comments')
    first_line = models.PositiveIntegerField(_(b'first line'), blank=True, null=True)
    num_lines = models.PositiveIntegerField(_(b'number of lines'), blank=True, null=True)
    last_line = property(lambda self: self.first_line + self.num_lines - 1)

    def get_absolute_url(self):
        revision_path = six.text_type(self.filediff.diffset.revision)
        if self.interfilediff:
            revision_path += b'-%s' % self.interfilediff.diffset.revision
        return b'%sdiff/%s/?file=%s#file%sline%s' % (
         self.get_review_request().get_absolute_url(),
         revision_path, self.filediff.id, self.filediff.id,
         self.first_line)

    class Meta(BaseComment.Meta):
        db_table = b'reviews_comment'
        verbose_name = _(b'Diff Comment')
        verbose_name_plural = _(b'Diff Comments')