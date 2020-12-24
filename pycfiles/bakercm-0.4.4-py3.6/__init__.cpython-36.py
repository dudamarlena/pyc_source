# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\baker\__init__.py
# Compiled at: 2018-11-12 13:46:47
# Size of source mod 2**32: 703 bytes
import sys
__version__ = '0.4.4'

def main():
    try:
        from baker.commands import execute_command_line
    except ImportError:
        try:
            import baker
        except ImportError:
            raise ImportError("Couldn't import Baker. Are you sure it's installed and available on your PYTHONPATH environment variable? Did you forget to activate a virtual environment?")

        raise

    execute_command_line(sys.argv)