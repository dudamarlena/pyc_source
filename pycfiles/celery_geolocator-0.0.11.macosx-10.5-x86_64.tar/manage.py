# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/examples/django_celery/manage.py
# Compiled at: 2014-08-09 13:41:56
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)