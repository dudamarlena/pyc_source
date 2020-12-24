# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/jobs/metrics/formatting.py
# Compiled at: 2018-04-20 03:19:42
"""Utilities related to formatting job metrics for human consumption."""

class JobMetricFormatter(object):
    """Format job metric key-value pairs for human consumption in Web UI."""

    def format(self, key, value):
        return (
         str(key), str(value))


def seconds_to_str(value):
    """Convert seconds to a simple simple string describing the amount of time."""
    if value < 60:
        return '%s seconds' % value
    else:
        if value < 3600:
            return '%s minutes' % (value / 60)
        return '%s hours and %s minutes' % (value / 3600, value % 3600 / 60)