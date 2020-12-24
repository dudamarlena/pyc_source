# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/slothauth/slothauth/utils.py
# Compiled at: 2016-07-08 21:10:28
# Size of source mod 2**32: 4328 bytes
from functools import wraps
import logging, random, string
from django.db import connections
from django.db import models
from django.db.models import EmailField
from django.db.models.signals import pre_migrate
from django.dispatch import receiver

def disable_for_loaddata(signal_handler):
    """
    Decorator that turns off signal handlers when loading fixture data.
    """

    @wraps(signal_handler)
    def wrapper(*args, **kwargs):
        if 'raw' in kwargs and kwargs['raw']:
            return
        signal_handler(*args, **kwargs)

    return wrapper


class InstanceDoesNotRequireFieldsMixin(object):
    __doc__ = ' Mixin that will only validate form fields that are being saved '

    def _clean_fields(self):
        if self.instance:
            for name, field in self.fields.items():
                if name not in self.data:
                    attr = getattr(self.instance, name)
                    if attr:
                        self.data[name] = attr

        return super(InstanceDoesNotRequireFieldsMixin, self)._clean_fields()

    def clean(self):
        if self.instance:
            for name, field in self.fields.items():
                if name not in self.cleaned_data:
                    attr = getattr(self.instance, name)
                    if attr:
                        self.cleaned_data[name] = attr

        return super(InstanceDoesNotRequireFieldsMixin, self).clean()


class RandomField(models.CharField):
    MAX_LOOPS = 10

    def __init__(self, seed=string.ascii_lowercase + string.digits, *args, **kwargs):
        self.seed = seed
        super(RandomField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, class_, key):
        super(RandomField, self).contribute_to_class(class_, key)
        models.signals.pre_save.connect(self.generate_unique, sender=class_)
        models.signals.post_migrate.connect(self.generate_unique, sender=class_)

    def generate_unique(self, sender, instance, *args, **kwargs):
        if not getattr(instance, self.attname):
            value = None
            for i in range(0, RandomField.MAX_LOOPS):
                value = ''.join(random.choice(self.seed) for x in range(self.max_length))
                if sender.objects.filter(**{self.name: value}).count() > 0:
                    value = None
                else:
                    break

            if i == RandomField.MAX_LOOPS:
                error = 'Could not generate a unique field for field %s.%s!' % (sender._meta.module_name, self.name)
                logging.error(error)
                return
            if i >= RandomField.MAX_LOOPS * 2 / 3:
                logging.warning('Looped 2/3 the max allowable loops for unique field on %s.%s consider upping the length of the keys' % (sender._meta.module_name, self.name))
            setattr(instance, self.attname, value)


try:
    unicode = unicode
except NameError:
    str = str
    unicode = str
    bytes = bytes
    basestring = (str, bytes)
else:
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

@receiver(pre_migrate)
def setup_postgres_extensions(sender, **kwargs):
    conn = connections[kwargs['using']]
    if conn.vendor == 'postgresql':
        cursor = conn.cursor()
        cursor.execute('CREATE EXTENSION IF NOT EXISTS citext')


class CiEmailField(EmailField):
    __doc__ = 'A case insensitive EmailField.\n    It uses the CITEXT extension on postgresql and lowercases the value on\n    other databases.\n    '

    def db_type(self, connection):
        if connection.vendor == 'postgresql':
            return 'CITEXT'
        return super(CiEmailField, self).db_type(connection)

    def get_db_prep_value(self, value, connection, prepared=False):
        if connection.vendor != 'postgresql' and isinstance(value, basestring):
            value = value.lower()
        return super(CiEmailField, self).get_db_prep_value(value, connection, prepared)