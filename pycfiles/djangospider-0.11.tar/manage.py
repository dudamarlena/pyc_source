# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/djangospider-0.1-py2.7.egg/djangospider/monitor/manage.py
# Compiled at: 2016-02-28 00:58:07
import os, sys
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitor.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)