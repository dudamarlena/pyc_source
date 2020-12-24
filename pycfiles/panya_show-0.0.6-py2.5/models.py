# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/show/models.py
# Compiled at: 2010-08-24 03:41:12
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from ckeditor.fields import RichTextField
from event.models import Event
from panya.models import ModelBase
from preferences.models import Preferences

class ShowContributor(ModelBase):
    profile = RichTextField(help_text='Full profile for this contributor.', blank=True, null=True)
    shows = models.ManyToManyField('show.Show', through='show.Credit', related_name='show_contributors')

    class Meta:
        verbose_name = 'Show contributor'
        verbose_name_plural = 'Show contributors'

    def get_absolute_url(self):
        return reverse('showcontributor_content_list', kwargs={'slug': self.slug})


class Credit(models.Model):
    contributor = models.ForeignKey('show.ShowContributor', related_name='credits')
    show = models.ForeignKey('show.Show', related_name='credits')
    role = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return '%s credit for %s' % (self.contributor.title, self.show.title)


class Show(ModelBase):
    content = RichTextField(help_text='Full article detailing this show.', blank=True, null=True)
    contributor = models.ManyToManyField('show.ShowContributor', through='show.Credit')

    def get_primary_contributors(self):
        """
        Returns a list of primary contributors, with primary being defined as those contributors that have the highest role assigned(in terms of priority). Only premitted contributors are returned.
        """
        primary_credits = []
        credits = self.credits.exclude(role=None).order_by('role')
        if credits:
            primary_role = credits[0].role
            for credit in credits:
                if credit.role == primary_role:
                    primary_credits.append(credit)

        contributors = []
        for credit in primary_credits:
            contributor = credit.contributor
            if contributor.is_permitted:
                contributors.append(contributor)

        return contributors

    def is_contributor_title_in_title(self, contributor):
        """
        Checks whether or not a contributors title is already present in the show's title.
        """
        return contributor.title.lower().lstrip().rstrip() in self.title.lower()


class RadioShow(Show):
    pass


class ShowPreferences(Preferences):
    __module__ = 'preferences.models'

    class Meta:
        verbose_name = 'Show preferences'
        verbose_name_plural = 'Show preferences'


class CreditOption(models.Model):
    show_preferences = models.ForeignKey('preferences.ShowPreferences')
    role_name = models.CharField(max_length=256, blank=True, null=True)
    role_priority = models.IntegerField(blank=True, null=True, help_text='The priority assigned to this role, with lower values being more importent.')


class Appearance(models.Model):
    event = models.ForeignKey(Event, related_name='appearances')
    show_contributor = models.ForeignKey(ShowContributor, related_name='appearances')