# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /botfly/autodebug.py
# Compiled at: 2019-10-27 21:16:49
# Size of source mod 2**32: 1136 bytes
__doc__ = '\nImporting this module sets up the Python interpreter to enter the botfly\ndebugger on an uncaught exception, rather than exiting.\n\nExample:\n\n    def main(argv):\n       # ...\n       return 0\n\n    # ...\n    if __name__ == "__main__":\n        from botfly import autodebug\n        sys.exit(main(sys.argv))\n\nNormally, if any exception is not caught it results in a stracktrace being\nprinted at the terminal and the program ending.\n\nAfter this import, an interactive debugger prompt will be started instead.\n'
import sys
from botfly import debugger
debugger.autodebug()