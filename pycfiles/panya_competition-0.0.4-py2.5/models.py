# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/competition/models.py
# Compiled at: 2010-08-04 03:48:25
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from ckeditor.fields import RichTextField
from panya.models import ModelBase
from preferences.models import Preferences

class Competition(ModelBase):
    content = RichTextField()
    start_date = models.DateField(blank=True, null=True, help_text='Date the competition starts.')
    end_date = models.DateField(blank=True, null=True, help_text='Date the competition ends.')
    question = models.CharField(blank=True, null=True, max_length=255, help_text='Short competition question')
    question_blurb = RichTextField(blank=True, null=True, help_text='Descriptive text elaborating on the question.')
    correct_answer = models.CharField(max_length=255, blank=True, null=True, help_text='Answer used to determine winning entries.')
    rules = RichTextField(blank=True, null=True, help_text='Rules specific to this competition.')

    def get_absolute_url(self):
        return reverse('competition_object_detail', kwargs={'slug': self.slug})

    def __unicode__(self):
        return self.title


class CompetitionEntry(models.Model):
    competition = models.ForeignKey(Competition, related_name='competition_entries')
    user = models.ForeignKey(User, related_name='competition_entries_users')
    answer = models.CharField(max_length=255)
    winner = models.BooleanField(help_text='Mark this competition entry as a winning entry.')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Competition entry'
        verbose_name_plural = 'Competition entries'

    def correct_answer(self):
        if self.answer and self.competition.correct_answer:
            return self.answer.lower() == self.competition.correct_answer.lower()
        return False

    def __unicode__(self):
        return '%s answered %s' % (self.user.username, self.answer)


class CompetitionPreferences(Preferences):
    __module__ = 'preferences.models'
    rules = RichTextField(blank=True, null=True, help_text='General rules which apply to all competitions.')

    class Meta:
        verbose_name = 'Competition preferences'
        verbose_name_plural = 'Competition preferences'