# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/processors/noop.py
# Compiled at: 2015-11-08 18:31:47
from tvrenamer.processors import base

class NoopResults(base.ResultProcessorBase):
    """Result processor that does nothing."""

    @property
    def priority(self):
        """Processor priority used for sorting to determine execution order."""
        return 1

    @property
    def enabled(self):
        """Determines if a processor plugin is enabled for processing data."""
        return True

    def process(self, data):
        """Process the results from episode processing.

        :param list data: result instances
        """
        pass