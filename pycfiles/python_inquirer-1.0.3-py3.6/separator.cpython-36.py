# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_inquirer/separator.py
# Compiled at: 2019-08-16 00:14:27
# Size of source mod 2**32: 247 bytes
"""
Used to space/separate choices group
"""

class Separator(object):
    line = '---------------'

    def __init__(self, line=None):
        if line:
            self.line = line

    def __str__(self):
        return self.line