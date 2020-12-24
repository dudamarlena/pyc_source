# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/connector/timestampvalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 343 bytes
__doc__ = 'pathelement.py\n\nCreated on: May 19, 2017\n    Author: Jeroen van der Heijden <jeroen@transceptor.technology>\n'

class TimestampValue:

    def __init__(self, timestamp_value):
        self._timestamp_value = timestamp_value

    def __str__(self):
        """Returns the formatted timestamp value."""
        return self._timestamp_value