# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/db/models/fields/jsonfield.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, unicode_literals
import json, datetime, six
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sentry.db.models.utils import Creator

def default(o):
    if hasattr(o, b'to_json'):
        return o.to_json()
    if isinstance(o, Decimal):
        return six.text_type(o)
    if isinstance(o, datetime.datetime):
        if o.tzinfo:
            return o.strftime(b'%Y-%m-%dT%H:%M:%S%z')
        return o.strftime(b'%Y-%m-%dT%H:%M:%S')
    if isinstance(o, datetime.date):
        return o.strftime(b'%Y-%m-%d')
    if isinstance(o, datetime.time):
        if o.tzinfo:
            return o.strftime(b'%H:%M:%S%z')
        return o.strftime(b'%H:%M:%S')
    raise TypeError(repr(o) + b' is not JSON serializable')


class JSONField(models.TextField):
    """
    A field that will ensure the data entered into it is valid JSON.

    Originally from https://github.com/adamchainz/django-jsonfield/blob/0.9.13/jsonfield/fields.py
    Adapted to fit our requirements of:

    - always using a text field
    - being able to serialize dates/decimals
    - not emitting deprecation warnings
    """
    default_error_messages = {b'invalid': _(b"'%s' is not a valid JSON string.")}
    description = b'JSON object'

    def __init__(self, *args, **kwargs):
        if not kwargs.get(b'null', False):
            kwargs[b'default'] = kwargs.get(b'default', dict)
        self.encoder_kwargs = {b'indent': kwargs.pop(b'indent', getattr(settings, b'JSONFIELD_INDENT', None))}
        super(JSONField, self).__init__(*args, **kwargs)
        self.validate(self.get_default(), None)
        return

    def contribute_to_class(self, cls, name):
        """
        Add a descriptor for backwards compatibility
        with previous Django behavior.
        """
        super(JSONField, self).contribute_to_class(cls, name)
        setattr(cls, name, Creator(self))

    def validate(self, value, model_instance):
        if not self.null and value is None:
            raise ValidationError(self.error_messages[b'null'])
        try:
            self.get_prep_value(value)
        except BaseException:
            raise ValidationError(self.error_messages[b'invalid'] % value)

        return

    def get_default(self):
        if self.has_default():
            default = self.default
            if callable(default):
                default = default()
            if isinstance(default, six.string_types):
                return json.loads(default)
            return json.loads(json.dumps(default))
        return super(JSONField, self).get_default()

    def get_internal_type(self):
        return b'TextField'

    def db_type(self, connection):
        return b'text'

    def to_python(self, value):
        if isinstance(value, six.string_types):
            if value == b'':
                if self.null:
                    return None
                if self.blank:
                    return b''
            try:
                value = json.loads(value)
            except ValueError:
                msg = self.error_messages[b'invalid'] % value
                raise ValidationError(msg)

        return value

    def get_db_prep_value(self, value, connection=None, prepared=None):
        return self.get_prep_value(value)

    def get_prep_value(self, value):
        if value is None:
            if not self.null and self.blank:
                return b''
            return
        return json.dumps(value, default=default, **self.encoder_kwargs)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('exact', 'iexact'):
            return self.to_python(self.get_prep_value(value))
        if lookup_type == b'in':
            return [ self.to_python(self.get_prep_value(v)) for v in value ]
        if lookup_type == b'isnull':
            return value
        if lookup_type in ('contains', 'icontains'):
            if isinstance(value, (list, tuple)):
                raise TypeError(b'Lookup type %r not supported with argument of %s' % (
                 lookup_type, type(value).__name__))
                return self.get_prep_value(value)[1:-1].replace(b', ', b'%')
            if isinstance(value, dict):
                return self.get_prep_value(value)[1:-1]
            return self.to_python(self.get_prep_value(value))
        raise TypeError(b'Lookup type %r not supported' % lookup_type)

    def value_to_string(self, obj):
        return self._get_val_from_obj(obj)


if b'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], [b'^sentry\\.db\\.models\\.fields\\.jsonfield.JSONField'])