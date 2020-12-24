# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /elicit/autodebug.py
# Compiled at: 2018-12-17 01:13:46
# Size of source mod 2**32: 1186 bytes
"""
Importing this module sets up the Python interpreter to enter the elicit
debugger on an uncaught exception, rather than exiting.

Example:

    def main(argv):
       # ...
       return 0

    # ...
    if __name__ == "__main__":
        from elicit import autodebug
        sys.exit(main(sys.argv))

Normally, if any exception is not caught it results in a stracktrace being
printed at the terminal and the program ending.

After this import, an interactive debugger prompt will be started instead.
"""
import sys
from elicit import debugger
debugger.autodebug()