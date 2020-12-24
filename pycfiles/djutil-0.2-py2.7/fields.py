# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\fields.py
# Compiled at: 2013-08-29 06:32:20
from __future__ import unicode_literals
from django.db.models import CharField
from django.utils.crypto import get_random_string, random
from django.utils import six
ALLOWED_CHARS = b'0123456789'

class CodeField(CharField):

    def __init__(self, *args, **kwargs):
        kwargs[b'max_length'] = kwargs.get(b'max_length', 5)
        kwargs[b'unique'] = kwargs.get(b'unique', True)
        if b'db_index' not in kwargs:
            kwargs[b'db_index'] = True
        self.allowed_range = kwargs.pop(b'allowed_range', None)
        self.allowed_chars = kwargs.pop(b'allowed_chars', ALLOWED_CHARS)
        self.manager = kwargs.pop(b'manager', None)
        super(CodeField, self).__init__(*args, **kwargs)
        return

    def pre_save(self, instance, add):
        value = self.value_from_object(instance)
        manager = self.manager
        if not value:
            value = generate_unique_code(self, instance, manager, length=self.max_length, allowed_range=self.allowed_range, allowed_chars=self.allowed_chars)
            setattr(instance, self.name, value)
        return value

    def south_field_triple(self):
        """Returns a suitable description of this field for South."""
        from south.modelsinspector import introspector
        args, kwargs = introspector(self)
        return (b'djutil.fields.CodeField', args, kwargs)


def generate_unique_code(field, instance, manager, length, allowed_range, allowed_chars):
    if not manager:
        manager = type(instance).objects
    for i in six.moves.xrange(1000):
        code = generate_code(length, allowed_range, allowed_chars)
        lookups = {(b'{}__iexact').format(field.name): code}
        rivals = manager.filter(**lookups).exclude(pk=instance.pk)
        if not rivals:
            return code

    raise ValueError((b'Could not generate unique code for model: {}').format(instance))


def generate_code(length=5, allowed_range=None, allowed_chars=ALLOWED_CHARS):
    """
    If allowed range is specified, select number from range [a, b] inclusively.
    Otherwise pick from allowed chars.
    """
    if allowed_range:
        return str(random.randint(*allowed_range))
    else:
        return get_random_string(length, allowed_chars)