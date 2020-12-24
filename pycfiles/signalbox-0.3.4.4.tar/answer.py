# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/models/answer.py
# Compiled at: 2014-08-27 19:26:12
from __future__ import unicode_literals
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe
from django.db import models
from django.conf import settings
from signalbox.utilities.djangobits import supergetattr
from ask.models import fields
from signalbox.exceptions import SignalBoxException

def upload_file_name(instance, filename):
    return (b'/').join([b'userdata', instance.reply.token, filename])


class Answer(models.Model):
    """Stores user questionnaire data."""

    def save(self, force_save=False, *args, **kwargs):
        if not force_save and not settings.USE_VERSIONING and self.pk:
            raise SignalBoxException(b'Editing answers is not allowed unless you enable version control')
        super(Answer, self).save(*args, **kwargs)

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (i, getattr(self, i))

    def __contains__(self, x):
        return x in getattr(self, b'answer')

    question = models.ForeignKey(b'ask.Question', blank=True, null=True, on_delete=models.PROTECT, help_text=b'The question this answer refers to')
    page = models.ForeignKey(b'ask.AskPage', blank=True, null=True, help_text=b'The page this question was displayed on', on_delete=models.PROTECT)
    other_variable_name = models.CharField(max_length=256, blank=True, null=True)
    choices = models.TextField(blank=True, null=True, help_text=b'JSON representation of the options the user could select from,\n        at the time the answer was saved.')
    answer = models.TextField(blank=True, null=True)
    upload = models.FileField(blank=True, null=True, storage=settings.USER_UPLOAD_STORAGE_BACKEND, upload_to=upload_file_name)
    reply = models.ForeignKey(b'signalbox.Reply', blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    meta = models.TextField(blank=True, null=True, help_text=b'Additional data as python dict serialised to JSON.')

    def mapped_score(self):
        """Return mapped score; leave answer unchanged if no map found."""
        possiblechoices = supergetattr(self, b'question.choiceset.get_choices', ())
        score_maptos = {i.score:i.mapped_score for i in possiblechoices}
        return score_maptos.get(self.answer, self.answer)

    def participant(self):
        """Return the user to whom the answer relates (maybe not the user who entered it)."""
        return supergetattr(self, b'reply.observation.dyad.user', None)

    @property
    def study(self):
        """Return the study this Answer was made in response to."""
        return supergetattr(self, b'reply.observation.dyad.study', None)

    def variable_name(self):
        if self.question:
            return self.question.variable_name
        else:
            return self.other_variable_name

    def possible_choices_json(self):
        return self.question and self.question.choices_as_json()

    def choice_label(self):
        """Returns the label of the original Choice object selected."""
        if not self.question:
            return self.answer

        def _get_label(number):
            try:
                return [ j for i, j in self.question.choices() if i == int(self.answer) ][0]
            except:
                return

            return

        return _get_label(self.answer) or self.answer

    def __unicode__(self):
        return smart_text((b'{} (page {}): {}').format(self.variable_name(), supergetattr(self, b'page.id', None), smart_text(self.answer)[:80]))

    def get_value_for_export(self):
        """Pre-process the answer in preparation for exporting as csv etc.

        The processing which occurs will depend on the field type and the methods
        described in ask.fields.
        """
        class_name = fields.class_name(supergetattr(self, b'question.q_type', b''))
        processor = getattr(getattr(fields, class_name), b'export_processor')
        return processor(self.answer)

    class Meta:
        verbose_name_plural = b'user answers'
        ordering = [b'question__variable_name']
        unique_together = ([b'other_variable_name', b'reply', b'page'], [b'question', b'reply', b'page'])
        app_label = b'signalbox'