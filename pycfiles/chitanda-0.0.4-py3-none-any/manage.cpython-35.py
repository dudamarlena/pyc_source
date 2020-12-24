# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/manage.py
# Compiled at: 2015-09-08 14:13:36
# Size of source mod 2**32: 260 bytes
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chisubmit.backend.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)