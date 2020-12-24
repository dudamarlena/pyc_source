# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/chisubmit/backend/manage.py
# Compiled at: 2015-09-08 14:13:36
# Size of source mod 2**32: 260 bytes
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chisubmit.backend.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)