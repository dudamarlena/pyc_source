# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/processors/printer.py
# Compiled at: 2015-11-08 18:31:47
import logging
from oslo_config import cfg
import six
from tvrenamer.common import table
from tvrenamer.processors import base
LOG = logging.getLogger(__name__)

class PrintResults(base.ResultProcessorBase):
    """Result processor that dumps output to screen from execution."""

    @property
    def priority(self):
        """Processor priority used for sorting to determine execution order."""
        return 5

    @property
    def enabled(self):
        """Determines if a processor plugin is enabled for processing data."""
        return LOG.isEnabledFor(logging.INFO) and cfg.CONF.console_output_enabled

    def process(self, data):
        """Process the results from episode processing.

        :param list data: result instances
        """
        fields = []
        for res in data:
            for epname, out in six.iteritems(res.status):
                fields.append([
                 out.get('state'),
                 epname,
                 out.get('formatted_filename'),
                 out.get('messages')])

        if fields:
            table.write_output(fields)