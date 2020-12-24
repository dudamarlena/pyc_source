# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/tests/manage.py
# Compiled at: 2020-04-15 06:20:40
# Size of source mod 2**32: 1299 bytes
import os, sys
sys.path[0] = os.path.dirname(sys.path[0])
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tests.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        try:
            import django
        except ImportError:
            raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?")
        else:
            raise
    else:
        execute_from_command_line(sys.argv)