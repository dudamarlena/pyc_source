# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/participation/models/comment.py
# Compiled at: 2015-03-02 10:21:03
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from nodeshot.core.base.models import BaseDate
from .base import UpdateCountsMixin

class Comment(UpdateCountsMixin, BaseDate):
    """
    Comment model
    """
    node = models.ForeignKey('nodes.Node')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    text = models.CharField(_('Comment text'), max_length=255)

    class Meta:
        app_label = 'participation'
        db_table = 'participation_comment'
        ordering = ['id']

    def __unicode__(self):
        return self.text

    def update_count(self):
        """ updates comment count """
        node_rating_count = self.node.rating_count
        node_rating_count.comment_count = self.node.comment_set.count()
        node_rating_count.save()

    def clean(self, *args, **kwargs):
        """
        Check if comments can be inserted for parent node or parent layer
        """
        if not self.pk:
            node = self.node
            if node.participation_settings.comments_allowed is False:
                raise ValidationError('Comments not allowed for this node')
            if 'nodeshot.core.layers' in settings.INSTALLED_APPS:
                layer = node.layer
                if layer.participation_settings.comments_allowed is False:
                    raise ValidationError('Comments not allowed for this layer')