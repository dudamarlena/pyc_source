# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Admin\Documents\GitHub\maintenance\django_vehicles_maintenance\manage.py
# Compiled at: 2015-01-05 21:15:22
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maintenance.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)