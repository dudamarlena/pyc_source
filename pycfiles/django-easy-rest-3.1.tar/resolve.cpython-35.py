# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jonatan/myprojects/django-easy-rest/easy_rest/test_framework/resolvers/resolve.py
# Compiled at: 2018-09-14 14:50:50
# Size of source mod 2**32: 1605 bytes
from django.conf import settings
import os

def get_app_path(app_name):
    """
    Returns app path from django apps
    :param app_name: the name of the app to search
    :return: app path
    """
    return os.path.join(settings.BASE_DIR, app_name)


def app_exists(app_name):
    """
    Validates if the app exists
    :param app_name: the app name to validate
    :return: True/False (Boolean)
    """
    return os.path.exists(get_app_path(app_name))


def get_tests_file(app_name, file_name, data=''):
    """
    Returns the app test file if exists else creates a new test
    file and return it path
    :param app_name: the app to search for test file in
    :param file_name: the file name
    :param data: the data of the test file
    :return: path of file (str), data (str)
    """
    if not app_exists(app_name):
        return (None, None)
    path = os.path.join(get_app_path(app_name), file_name)
    if not os.path.exists(path):
        with open(path, 'w+') as (file):
            file.write(data)
    else:
        with open(path, 'r') as (file):
            data = file.read()
    return (
     path, data)


def register_unittest():
    """
    Register django env to know it's under a test
    :return: None
    """
    os.environ['under_test'] = 'True'


def in_test():
    """
    Check if django is under a test
    :return: True/False (boolean)
    """
    return bool(os.environ.get('under_test'))