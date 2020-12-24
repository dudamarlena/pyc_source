# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/iwoca/django-seven/django_seven/deprecated_rules/helpers.py
# Compiled at: 2016-07-26 15:41:40
import os, re
from django.conf import settings
SEVEN_EXCLUDED_DIRS = getattr(settings, 'SEVEN_EXCLUDED_DIRS', [])
SEVEN_EXCLUDED_SUB_PATHS = getattr(settings, 'SEVEN_EXCLUDED_SUB_PATHS', [])
SEVEN_EXCLUDED_SPECIFIC_FILE = getattr(settings, 'SEVEN_EXCLUDED_SPECIFIC_FILE', [])
SEVEN_EXCLUDED_FILE_EXTENSIONS = getattr(settings, 'SEVEN_EXCLUDED_FILE_EXTENSIONS', [])

def is_excluded_dir(dir_name):
    return any([ excluded_subpath in dir_name for excluded_subpath in SEVEN_EXCLUDED_SUB_PATHS ]) or any([ dir_name.startswith('./' + excluded_dir) for excluded_dir in SEVEN_EXCLUDED_DIRS ])


def is_excluded_file(file_name, dir_name):
    full_file_name = os.path.join(dir_name, file_name)
    return any([ file_name.endswith(excluded_file) for excluded_file in SEVEN_EXCLUDED_FILE_EXTENSIONS ]) or any([ excluded_file in full_file_name for excluded_file in SEVEN_EXCLUDED_SPECIFIC_FILE ])


def compile_regex(regex_rules):
    for rule in regex_rules:
        rule['compiled_regex'] = re.compile(rule['regex'])

    return regex_rules