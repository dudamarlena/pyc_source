# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.core/pyqode/core/widgets/pty_wrapper.py
# Compiled at: 2016-12-29 05:31:31
# Size of source mod 2**32: 476 bytes
import sys, os

def pty_wrapper_main():
    """
    Main function of the pty wrapper script
    """
    sys.path.insert(0, os.path.dirname(__file__))
    import _pty
    _pty.spawn(sys.argv[1:])


if __name__ == '__main__':
    pty_wrapper_main()