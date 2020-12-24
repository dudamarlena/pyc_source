# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/annotateme/standalone/manage.py
# Compiled at: 2018-11-12 05:28:42
# Size of source mod 2**32: 493 bytes
import os, sys

def main():
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        try:
            raise ImportError("Couldn't import Django. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?") from exc
        finally:
            exc = None
            del exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()