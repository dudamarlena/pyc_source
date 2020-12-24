# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/delucks/.pyenv/versions/3.8.1/lib/python3.8/site-packages/todo/exceptions.py
# Compiled at: 2019-12-22 12:59:22
# Size of source mod 2**32: 242 bytes


class GTDException(Exception):
    __doc__ = 'single parameter indicates exit code for the interpreter, because\n    this exception typically results in a return of control to the terminal'

    def __init__(self, errno):
        self.errno = errno