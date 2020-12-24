# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/wheel/wheel/__main__.py
# Compiled at: 2019-02-06 16:42:33
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