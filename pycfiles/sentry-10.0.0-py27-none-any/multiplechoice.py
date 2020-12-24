# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/fields/multiplechoice.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers

class MultipleChoiceField(serializers.Field):
    error_messages = {'invalid_choice': 'Select a valid choice. {value} is not one of the available choices.'}

    def __init__(self, choices=None, *args, **kwargs):
        self.choices = set(choices or ())
        super(MultipleChoiceField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        if isinstance(data, list):
            for item in data:
                if item not in self.choices:
                    raise serializers.ValidationError(self.error_messages['invalid_choice'].format(value=item))

            return data
        raise serializers.ValidationError('Please provide a valid list.')