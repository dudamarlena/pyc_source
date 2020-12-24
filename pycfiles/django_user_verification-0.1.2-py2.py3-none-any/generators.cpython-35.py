# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pauloostenrijk/WebProjects/django-user-verification/verification/generators.py
# Compiled at: 2016-05-20 11:07:56
# Size of source mod 2**32: 977 bytes
import random
from django.conf import settings
from django.utils.module_loading import import_string
DEFAULT_GENERATOR = 'verification.generators.NumberGenerator'

def get_generator(service_name):
    """
    Get the generator that is set for the specific service.
    """
    if not settings.USER_VERIFICATION.get(service_name, None):
        raise ValueError('{} not a valid service.'.format(service_name))
    service_settings = settings.USER_VERIFICATION.get(service_name)
    generator_path = service_settings.get('GENERATOR', DEFAULT_GENERATOR)
    return import_string(generator_path)()


class Generator(object):
    pass


class NumberGenerator(Generator):
    __doc__ = '\n    Creates a random number.\n\n    :usage example:\n        generator = NumberGenerator()\n        print(generator())  # 123923\n    '

    def __call__(self, key):
        return str(random.randint(10000, 99999))