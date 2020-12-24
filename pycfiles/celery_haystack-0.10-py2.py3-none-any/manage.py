# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/brent/anaconda/envs/fba/lib/python2.7/site-packages/examples/django_celery/manage.py
# Compiled at: 2014-08-09 13:41:56
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)