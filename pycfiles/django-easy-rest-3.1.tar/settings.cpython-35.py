# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jonatan/myprojects/django-easy-rest/easy_rest/test_framework/resolvers/settings.py
# Compiled at: 2017-12-21 15:16:33
# Size of source mod 2**32: 1137 bytes
from django.conf import settings as django_settings

def get_override_settings(attributes=None):
    """
    Overrides settings by attribute keys
    :param attributes: attribute = keys of dictionary
    :return: built override settings
    """
    if not attributes:
        attributes = []
    if not django_settings._wrapped:
        django_settings._setup()
    settings = django_settings._wrapped
    return build_str({key:val for key, val in settings.__dict__.items() if key in attributes})


def build_str(dictionary_to_build_from):
    """
    Building override string
    :param dictionary_to_build_from:  what to build from
    :return: built string
    """
    built = ''
    for key, val in dictionary_to_build_from.items():
        built += '{key}={val},'.format(key=key, val=val)

    return built[:-1]