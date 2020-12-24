# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/participation/models/vote.py
# Compiled at: 2015-03-02 10:21:03
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.exceptions import ValidationError
from nodeshot.core.base.models import BaseDate
from .base import UpdateCountsMixin

class Vote(UpdateCountsMixin, BaseDate):
    """
    Vote model
    Like or dislike feature
    """
    VOTING_CHOICES = (
     (1, 'Like'),
     (-1, 'Dislike'))
    node = models.ForeignKey('nodes.Node')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    vote = models.IntegerField(choices=VOTING_CHOICES)

    class Meta:
        app_label = 'participation'

    def __unicode__(self):
        if self.pk:
            return _('vote #%d for node %s') % (self.pk, self.node.name)
        else:
            return _('vote')

    def save(self, *args, **kwargs):
        """
        ensure users cannot vote the same node multiple times
        but let users change their votes
        """
        if not self.pk:
            old_votes = Vote.objects.filter(user=self.user, node=self.node)
            for old_vote in old_votes:
                old_vote.delete()

        super(Vote, self).save(*args, **kwargs)

    def update_count(self):
        """ updates likes and dislikes count """
        node_rating_count = self.node.rating_count
        node_rating_count.likes = self.node.vote_set.filter(vote=1).count()
        node_rating_count.dislikes = self.node.vote_set.filter(vote=-1).count()
        node_rating_count.save()

    def clean(self, *args, **kwargs):
        """
        Check if votes can be inserted for parent node or parent layer
        """
        if not self.pk:
            if self.node.participation_settings.voting_allowed is not True:
                raise ValidationError('Voting not allowed for this node')
            if 'nodeshot.core.layers' in settings.INSTALLED_APPS:
                layer = self.node.layer
                if layer.participation_settings.voting_allowed is not True:
                    raise ValidationError('Voting not allowed for this layer')