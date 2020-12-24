# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/generic/managers.py
# Compiled at: 2016-05-21 00:29:27
from __future__ import unicode_literals
from django.contrib.comments.managers import CommentManager as DjangoCM
from django.db.models import Manager
from shuyucms.conf import settings

class CommentManager(DjangoCM):
    """
    Provides filter for restricting comments that are not approved
    if ``COMMENTS_UNAPPROVED_VISIBLE`` is set to ``False``.
    """

    def visible(self):
        """
        Return the comments that are visible based on the
        ``COMMENTS_XXX_VISIBLE`` settings. When these settings
        are set to ``True``, the relevant comments are returned
        that shouldn't be shown, and are given placeholders in
        the template ``generic/includes/comment.html``.
        """
        settings.use_editable()
        visible = self.all()
        if not settings.COMMENTS_REMOVED_VISIBLE:
            visible = visible.filter(is_removed=False)
        return visible

    def count_queryset(self):
        """
        Called from ``CommentsField.related_items_changed`` to store
        the comment count against an item each time a comment is saved.
        """
        return self.visible().count()


class KeywordManager(Manager):

    def get_by_natural_key(self, value):
        """
        Provides natural key method.
        """
        return self.get(value=value)

    def get_or_create_iexact(self, **kwargs):
        """
        Case insensitive title version of ``get_or_create``. Also
        allows for multiple existing results.
        """
        lookup = dict(**kwargs)
        try:
            lookup[b'title__iexact'] = lookup.pop(b'title')
        except KeyError:
            pass

        try:
            return (
             self.filter(**lookup)[0], False)
        except IndexError:
            return (
             self.create(**kwargs), True)