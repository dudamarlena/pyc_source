# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jstutters/.virtualenvs/pirec/lib/python3.6/site-packages/pirec/recorders/stdout.py
# Compiled at: 2017-02-10 11:03:57
# Size of source mod 2**32: 483 bytes
"""Exposes the StdOut recorder."""
from __future__ import print_function

class StdOut(object):
    __doc__ = 'Print results to stdout.\n\n    Args:\n        values (dict): key-value pairs to be printed\n    '

    def __init__(self, values):
        """Initialize the recorder."""
        self.values = values

    def write(self, results):
        """Print the results to stdout."""
        for field in self.values:
            print('{0}: {1}'.format(field, self.values[field](results)))