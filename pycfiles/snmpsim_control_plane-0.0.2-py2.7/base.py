# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim_control_plane/supervisor/reporting/formats/base.py
# Compiled at: 2020-01-30 12:14:23


class BaseReporter(object):
    """Maintain activity metrics.
    """

    def __init__(self, *args, **kwargs):
        pass

    def dump_metrics(self, metrics, watch_dir=None, started=None, begin=None, end=None):
        """Dump metrics in a reporter-specific way.
        """
        pass

    def __str__(self):
        return self.__class__.__name__