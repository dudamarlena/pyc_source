# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/membership.py
# Compiled at: 2014-08-27 19:26:12
from datetime import datetime
import itertools
from django.conf import settings
from answer import Answer
from contracts import contract
from django.db import models
from observation import Observation
from signalbox.utilities.linkedinline import admin_edit_url
from signalbox.utils import proportion

class MembershipManager(models.Manager):

    def authorised(self, user):
        """Provide per-user access for Memberships.

        No-op at present."""
        qs = super(MembershipManager, self).select_related()
        return qs


class Membership(models.Model):
    """Users join Studies which is recorded in a Membership object. """
    objects = MembershipManager()
    active = models.BooleanField(default=True, help_text='If deselected, Observations no longer be sent for Membership.', db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='The person providing data, normally the participant.')
    study = models.ForeignKey('signalbox.Study')
    relates_to = models.ForeignKey('signalbox.Membership', blank=True, null=True, verbose_name='Linked patient', related_name='membership_relates_to', help_text='Sometimes a researcher may themselves become a subject in a study (for\n        example to provide ratings of different patients progress). In this instance they may\n        be added to the study multiple times, with the relates_to field set to another User,\n        for which they are providing data.')
    condition = models.ForeignKey('signalbox.StudyCondition', null=True, blank=True, help_text='Choose a Study/Condition for this user. To use Randomisation you must\n        save the Membership first, then randomise to a condition using the tools menu (or\n        if set, the study may auto-randomise the participant).')
    date_joined = models.DateField(auto_now_add=True)
    date_randomised = models.DateField(null=True, blank=True)

    @contract
    def ad_hoc_askers_and_last_replies(self):
        """
        :returns: A list of tuples containing the asker and the replies made within this membership.
        :rtype: list(tuple)
        """
        askers = self.study.ad_hoc_askers.all()
        return [ (i, self.reply_set.filter(asker=i)) for i in askers ]

    def save(self, *args, **kwargs):
        if self.condition:
            self.study = self.condition.study
        super(Membership, self).save(*args, **kwargs)

    def is_current(self):
        """Return True if the user has outstanding observations within a study."""
        obs = self.observation_set.all()
        return bool([ o.status != 1 for o in obs ]) and self.active

    def observations(self):
        """Return the observations for this Membership.
        """
        obs = self.observation_set.select_related()
        return obs

    def incomplete_observations(self):
        return self.observations().exclude(status=1)

    def has_observation_expiring_today(self):
        return sum([ i.expires_today() for i in self.observations() ])

    outcomes = lambda self: self.observations(threshold=50)
    outcomes_due = lambda self: [ i for i in self.outcomes() if i.due < datetime.now() ]
    outcomes_complete = lambda self: [ i for i in self.outcomes() if i.status == 1 ]
    outcomes_due_complete = lambda self: [ i for i in self.outcomes_due() if i.status == 1 ]
    prop_outcomes_complete = lambda self: proportion(len(self.outcomes_complete()), len(self.outcomes()))
    prop_outcomes_due_complete = lambda self: proportion(len(self.outcomes_due_complete()), len(self.outcomes_due()))

    def randomised(self):
        return bool(self.condition)

    def make_ad_hoc_observation(self):
        """Make an ad hoc Observation, save it, and return it."""
        rightnow = datetime.now()
        newobs = Observation(status=-1, dyad=self, due=rightnow, due_original=rightnow, label='Ad hoc observation')
        newobs.save()
        return newobs

    def add_observations(self):
        """Creates and saves Observations -> [Observation]."""
        if not self.condition:
            return []
        observations = []
        observations = itertools.chain(*[ s.make_observations(membership=self) for s in self.condition.scripts.all() ])
        self.save()
        return observations

    def questions_answered(self):
        return Answer.objects.filter(reply__observation__in=self.observation_set.all()).count()

    def admin_edit_url(self):
        return admin_edit_url(self)

    class Meta:
        permissions = (
         ('can_add_observations', 'Can generate observations for a membership'),
         ('can_randomise_user', 'Can randomise a user'))
        verbose_name = 'Study membership'
        app_label = 'signalbox'
        ordering = ['-date_randomised']

    def __unicode__(self):
        string = getattr(self, 'study', 'None')
        return '%s, member of %s' % (self.user.username, string)