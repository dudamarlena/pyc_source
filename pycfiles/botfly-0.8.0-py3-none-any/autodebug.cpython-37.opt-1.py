# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /botfly/autodebug.py
# Compiled at: 2019-10-27 21:16:49
# Size of source mod 2**32: 1136 bytes
"""
Importing this module sets up the Python interpreter to enter the botfly
debugger on an uncaught exception, rather than exiting.

Example:

    def main(argv):
       # ...
       return 0

    # ...
    if __name__ == "__main__":
        from botfly import autodebug
        sys.exit(main(sys.argv))

Normally, if any exception is not caught it results in a stracktrace being
printed at the terminal and the program ending.

After this import, an interactive debugger prompt will be started instead.
"""
import sys
from botfly import debugger
debugger.autodebug()