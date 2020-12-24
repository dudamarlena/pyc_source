# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dpl1_main/manage.py
# Compiled at: 2014-02-28 04:59:17
import os, sys
current_dir = os.getcwd()
sys.path.remove(current_dir)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))
print sys.path
try:
    from deployment_util import correct_sys_path
except ImportError:
    pass

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dpl1_main.DPL1.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)