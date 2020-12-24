# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/wheel/wheel/__main__.py
# Compiled at: 2019-07-30 18:46:56
# Size of source mod 2**32: 417 bytes
"""
Wheel command line tool (enable python -m wheel syntax)
"""
import sys

def main():
    if __package__ == '':
        import os.path
        path = os.path.dirname(os.path.dirname(__file__))
        sys.path[0:0] = [path]
    import wheel.cli
    sys.exit(wheel.cli.main())


if __name__ == '__main__':
    sys.exit(main())