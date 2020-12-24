# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/poll/models.py
# Compiled at: 2015-04-21 15:32:20
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import ugettext_lazy as _
from secretballot.models import Vote
from jmbo.models import ModelBase

class Poll(ModelBase):
    votes_enabled = models.BooleanField(verbose_name=_('Voting enabled'), help_text=_('Enable voting for this item. The vote form will not display when disabled.'), default=True)
    anonymous_votes = models.BooleanField(verbose_name=_('Anonymous voting enabled'), help_text=_('Enable anonymous voting for this item.'), default=True)
    votes_closed = models.BooleanField(verbose_name=_('Voting closed'), help_text=_("Close voting for this item. Votes results will still display, but users won't be able to add new votes."), default=False)

    def can_vote_on_poll(self, request):
        """Based on jmbo.models.can_vote."""
        if self.votes_closed:
            return (False, 'closed')
        else:
            if not self.votes_enabled:
                return (False, 'disabled')
            if not request.user.is_authenticated() and not self.anonymous_votes:
                return (False, 'auth_required')
            votes = Vote.objects.filter(object_id__in=[ o.id for o in self.polloption_set.all() ], token=request.secretballot_token)
            if votes.exists():
                return (False, 'voted')
            return (True, 'can_vote')

    @property
    def vote_count(self):
        """
        Returns the total number of votes cast across all the
        poll's options.
        """
        return Vote.objects.filter(content_type=ContentType.objects.get(app_label='poll', model='polloption'), object_id__in=[ o.id for o in self.polloption_set.all() ]).aggregate(Sum('vote'))['vote__sum'] or 0


class PollOption(models.Model):
    title = models.CharField(max_length=255)
    poll = models.ForeignKey(Poll)
    is_correct_answer = models.BooleanField(default=False, help_text='Is this option the correct answer?')

    def __unicode__(self):
        return '%s - %s' % (self.poll.title, self.title)

    @property
    def vote_count(self):
        """
        Returns the total number of votes cast for this
        poll options.
        """
        return Vote.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id).aggregate(Sum('vote'))['vote__sum'] or 0

    def percentage(self):
        """
        Returns the percentage of votes cast for this poll option in
        relation to all of its poll's other options.
        """
        total_vote_count = self.poll.vote_count
        if total_vote_count:
            return self.vote_count * 100.0 / total_vote_count
        return 0

    class Meta:
        ordering = ('pk', )