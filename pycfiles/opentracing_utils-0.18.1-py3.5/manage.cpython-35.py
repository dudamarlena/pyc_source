# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_django/manage.py
# Compiled at: 2019-02-13 08:31:21
# Size of source mod 2**32: 206 bytes
import os, sys
from django.core.management import execute_from_command_line
if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    execute_from_command_line(sys.argv)