# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/admin/Desktop/package_env/django_confirm_phone/phonenumber_confirmation/utils.py
# Compiled at: 2020-04-03 07:54:35
# Size of source mod 2**32: 1185 bytes
from django.core.exceptions import FieldError
from django.db.models import IntegerField
from random import randint

class RandomPinField(IntegerField):
    __doc__ = '\n    Generates a random digit pin\n\n    By default sets length=6\n\n    Optional arguments:\n        length\n            Integer for how long the pin will be. (default=4)\n    '

    def __init__(self, length=6, *args, **kwargs):
        self.length = length
        (super(RandomPinField, self).__init__)(*args, **kwargs)

    def generate_pin(self, model_instance):
        """
        Returns a random pin.
        """
        range_start = 10 ** (self.length - 1)
        range_end = 10 ** self.length - 1
        return randint(range_start, range_end)

    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if not value:
            value = self.generate_pin(model_instance)
            setattr(model_instance, self.attname, value)
        return value

    def deconstruct(self):
        name, path, args, kwargs = super(RandomPinField, self).deconstruct()
        if self.length != 4:
            kwargs['length'] = self.length
        return (
         name, path, args, kwargs)