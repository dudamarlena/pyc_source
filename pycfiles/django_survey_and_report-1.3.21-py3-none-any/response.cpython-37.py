# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/workspace/django-survey/survey/models/response.py
# Compiled at: 2020-02-22 08:00:49
# Size of source mod 2**32: 1305 bytes
from django.contrib.auth.models import User
from django.db import models
import django.utils.translation as _
from .survey import Survey
try:
    from django.conf import settings
    if settings.AUTH_USER_MODEL:
        user_model = settings.AUTH_USER_MODEL
    else:
        user_model = User
except (ImportError, AttributeError):
    user_model = User

class Response(models.Model):
    __doc__ = '\n        A Response object is a collection of questions and answers with a\n        unique interview uuid.\n    '
    created = models.DateTimeField((_('Creation date')), auto_now_add=True)
    updated = models.DateTimeField((_('Update date')), auto_now=True)
    survey = models.ForeignKey(Survey, on_delete=(models.CASCADE), verbose_name=(_('Survey')), related_name='responses')
    user = models.ForeignKey(user_model, on_delete=(models.SET_NULL), verbose_name=(_('User')), null=True, blank=True)
    interview_uuid = models.CharField((_('Interview unique identifier')), max_length=36)

    class Meta:
        verbose_name = _('Set of answers to surveys')
        verbose_name_plural = _('Sets of answers to surveys')

    def __str__(self):
        msg = 'Response to {} by {}'.format(self.survey, self.user)
        msg += ' on {}'.format(self.created)
        return msg