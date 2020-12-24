# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/django-hstore/django_hstore/forms.py
# Compiled at: 2015-06-29 10:27:05
# Size of source mod 2**32: 4182 bytes
from __future__ import unicode_literals, absolute_import
import json
from django.forms import Field
from django.utils import six
from django.utils.translation import ugettext
from django.core.exceptions import ValidationError
from .widgets import AdminHStoreWidget
from . import utils

def validate_hstore(value, is_serialized=False):
    """ HSTORE validation. """
    if value is None or value == '' or value == 'null':
        value = '{}'
    try:
        if isinstance(value, six.string_types):
            dictionary = json.loads(value)
            if is_serialized:
                if isinstance(dictionary, dict):
                    dictionary = dict((k, json.loads(v)) for k, v in dictionary.items())
        else:
            dictionary = value
    except ValueError as e:
        raise ValidationError(ugettext('Invalid JSON: {0}').format(e))

    if not isinstance(dictionary, dict):
        raise ValidationError(ugettext('No lists or values allowed, only dictionaries'))
    for key, value in dictionary.items():
        if isinstance(value, dict) or isinstance(value, list):
            dictionary[key] = json.dumps(value)
        if isinstance(value, bool) or isinstance(value, int) or isinstance(value, float):
            if not is_serialized:
                dictionary[key] = six.text_type(value).lower()
            else:
                continue

    return dictionary


class JsonMixin(object):

    def to_python(self, value):
        return validate_hstore(value)

    def render(self, name, value, attrs=None):
        if value:
            if not isinstance(value, six.string_types):
                value = json.dumps(value, sort_keys=True, indent=4)
        return super(JsonMixin, self).render(name, value, attrs)


class SerializedJsonMixin(JsonMixin):

    def to_python(self, value):
        return validate_hstore(value, is_serialized=True)

    def render(self, name, value, attrs=None):
        if isinstance(value, dict):
            value = dict((k, json.dumps(v)) for k, v in value.items())
        if value:
            if not isinstance(value, six.string_types):
                value = json.dumps(value, sort_keys=True, indent=4)
        return super(SerializedJsonMixin, self).render(name, value, attrs)


class DictionaryFieldWidget(JsonMixin, AdminHStoreWidget):
    pass


class SerializedDictionaryFieldWidget(SerializedJsonMixin, AdminHStoreWidget):
    pass


class ReferencesFieldWidget(JsonMixin, AdminHStoreWidget):

    def render(self, name, value, attrs=None):
        value = utils.serialize_references(value)
        return super(ReferencesFieldWidget, self).render(name, value, attrs)


class DictionaryField(JsonMixin, Field):
    __doc__ = '\n    A dictionary form field.\n    '

    def __init__(self, **params):
        params['widget'] = params.get('widget', DictionaryFieldWidget)
        super(DictionaryField, self).__init__(**params)


class SerializedDictionaryField(SerializedJsonMixin, Field):
    __doc__ = '\n    Serialized dictionary field.\n    '

    def __init__(self, **params):
        params['widget'] = params.get('widget', SerializedDictionaryFieldWidget)
        super(SerializedDictionaryField, self).__init__(**params)


class ReferencesField(JsonMixin, Field):
    __doc__ = '\n    A references form field.\n    '

    def __init__(self, **params):
        params['widget'] = params.get('widget', ReferencesFieldWidget)
        super(ReferencesField, self).__init__(**params)

    def to_python(self, value):
        value = super(ReferencesField, self).to_python(value)
        return utils.unserialize_references(value)