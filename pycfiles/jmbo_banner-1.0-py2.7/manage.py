# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/banner/tests/manage.py
# Compiled at: 2018-01-09 13:54:21
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banner.tests.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)