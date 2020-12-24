# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/connector/timestampvalue.py
# Compiled at: 2019-09-11 07:21:09
# Size of source mod 2**32: 343 bytes
"""pathelement.py

Created on: May 19, 2017
    Author: Jeroen van der Heijden <jeroen@transceptor.technology>
"""

class TimestampValue:

    def __init__(self, timestamp_value):
        self._timestamp_value = timestamp_value

    def __str__(self):
        """Returns the formatted timestamp value."""
        return self._timestamp_value