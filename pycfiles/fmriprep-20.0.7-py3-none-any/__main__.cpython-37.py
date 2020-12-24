# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/wheel/wheel/__main__.py
# Compiled at: 2020-05-05 12:41:36
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