# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/rules/conditions/tagged_event.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from collections import OrderedDict
from django import forms
from sentry import tagstore
from sentry.rules.conditions.base import EventCondition

class MatchType(object):
    EQUAL = 'eq'
    NOT_EQUAL = 'ne'
    STARTS_WITH = 'sw'
    ENDS_WITH = 'ew'
    CONTAINS = 'co'
    NOT_CONTAINS = 'nc'


MATCH_CHOICES = OrderedDict([
 (
  MatchType.EQUAL, 'equals'),
 (
  MatchType.NOT_EQUAL, 'does not equal'),
 (
  MatchType.STARTS_WITH, 'starts with'),
 (
  MatchType.ENDS_WITH, 'ends with'),
 (
  MatchType.CONTAINS, 'contains'),
 (
  MatchType.NOT_CONTAINS, 'does not contain')])

class TaggedEventForm(forms.Form):
    key = forms.CharField(widget=forms.TextInput())
    match = forms.ChoiceField(MATCH_CHOICES.items(), widget=forms.Select())
    value = forms.CharField(widget=forms.TextInput())


class TaggedEventCondition(EventCondition):
    form_cls = TaggedEventForm
    label = "An event's tags match {key} {match} {value}"
    form_fields = {'key': {'type': 'string', 'placeholder': 'key'}, 'match': {'type': 'choice', 'choices': MATCH_CHOICES.items()}, 'value': {'type': 'string', 'placeholder': 'value'}}

    def passes(self, event, state, **kwargs):
        key = self.get_option('key')
        match = self.get_option('match')
        value = self.get_option('value')
        if not (key and match and value):
            return False
        value = value.lower()
        key = key.lower()
        tags = (v.lower() for k, v in event.tags if k.lower() == key or tagstore.get_standardized_key(k) == key)
        if match == MatchType.EQUAL:
            for t_value in tags:
                if t_value == value:
                    return True

            return False
        if match == MatchType.NOT_EQUAL:
            for t_value in tags:
                if t_value == value:
                    return False

            return True
        if match == MatchType.STARTS_WITH:
            for t_value in tags:
                if t_value.startswith(value):
                    return True

            return False
        if match == MatchType.ENDS_WITH:
            for t_value in tags:
                if t_value.endswith(value):
                    return True

            return False
        if match == MatchType.CONTAINS:
            for t_value in tags:
                if value in t_value:
                    return True

            return False
        if match == MatchType.NOT_CONTAINS:
            for t_value in tags:
                if value in t_value:
                    return False

            return True

    def render_label(self):
        data = {'key': self.data['key'], 
           'value': self.data['value'], 
           'match': MATCH_CHOICES[self.data['match']]}
        return self.label.format(**data)