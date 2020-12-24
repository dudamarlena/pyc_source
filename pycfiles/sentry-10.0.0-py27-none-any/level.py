# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/rules/conditions/level.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from collections import OrderedDict
from django import forms
from sentry.constants import LOG_LEVELS, LOG_LEVELS_MAP
from sentry.rules.conditions.base import EventCondition
LEVEL_CHOICES = OrderedDict([ (('{0}').format(k), v) for k, v in sorted(LOG_LEVELS.items(), key=lambda x: x[0], reverse=True)
                            ])

class MatchType(object):
    EQUAL = 'eq'
    LESS_OR_EQUAL = 'lte'
    GREATER_OR_EQUAL = 'gte'


MATCH_CHOICES = OrderedDict([
 (
  MatchType.EQUAL, 'equal to'),
 (
  MatchType.LESS_OR_EQUAL, 'less than or equal to'),
 (
  MatchType.GREATER_OR_EQUAL, 'greater than or equal to')])

class LevelEventForm(forms.Form):
    level = forms.ChoiceField(choices=LEVEL_CHOICES.items())
    match = forms.ChoiceField(choices=MATCH_CHOICES.items())


class LevelCondition(EventCondition):
    form_cls = LevelEventForm
    label = "An event's level is {match} {level}"
    form_fields = {'level': {'type': 'choice', 'choices': LEVEL_CHOICES.items()}, 'match': {'type': 'choice', 'choices': MATCH_CHOICES.items()}}

    def passes(self, event, state, **kwargs):
        desired_level = self.get_option('level')
        desired_match = self.get_option('match')
        if not (desired_level and desired_match):
            return False
        desired_level = int(desired_level)
        try:
            level = LOG_LEVELS_MAP[event.get_tag('level')]
        except KeyError:
            return False

        if desired_match == MatchType.EQUAL:
            return level == desired_level
        if desired_match == MatchType.GREATER_OR_EQUAL:
            return level >= desired_level
        if desired_match == MatchType.LESS_OR_EQUAL:
            return level <= desired_level
        return False

    def render_label(self):
        data = {'level': LEVEL_CHOICES[self.data['level']], 
           'match': MATCH_CHOICES[self.data['match']]}
        return self.label.format(**data)