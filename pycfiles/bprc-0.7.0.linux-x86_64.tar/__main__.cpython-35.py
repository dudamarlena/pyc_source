# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/bprc/__main__.py
# Compiled at: 2016-08-20 13:14:45
# Size of source mod 2**32: 492 bytes
"""The main entry point. Invoke as `bprc' or `python3 -m bprc'."""
import sys, os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from bprc.core import main
if __name__ == '__main__':
    sys.exit(main())