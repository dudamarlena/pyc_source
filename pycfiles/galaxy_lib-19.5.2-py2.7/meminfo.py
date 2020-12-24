# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/jobs/metrics/instrumenters/meminfo.py
# Compiled at: 2018-09-15 08:40:24
"""The module describes the ``meminfo`` job metrics plugin."""
import re, sys
from galaxy import util
from . import InstrumentPlugin
from .. import formatting
if sys.version_info > (3, ):
    long = int
MEMINFO_LINE = re.compile('(\\w+)\\s*\\:\\s*(\\d+) kB')
MEMINFO_TITLES = {'memtotal': 'Total System Memory', 
   'swaptotal': 'Total System Swap'}

class MemInfoFormatter(formatting.JobMetricFormatter):

    def format(self, key, value):
        title = MEMINFO_TITLES.get(key, key)
        return (title, util.nice_size(value * 1000))


class MemInfoPlugin(InstrumentPlugin):
    """ Gather information about processor configuration from /proc/cpuinfo.
    Linux only.
    """
    plugin_type = 'meminfo'
    formatter = MemInfoFormatter()

    def __init__(self, **kwargs):
        self.verbose = util.asbool(kwargs.get('verbose', False))

    def pre_execute_instrument(self, job_directory):
        return "cat /proc/meminfo > '%s'" % self.__instrument_meminfo_path(job_directory)

    def job_properties(self, job_id, job_directory):
        properties = {}
        with open(self.__instrument_meminfo_path(job_directory)) as (f):
            for line in f:
                line = line.strip()
                if not line:
                    continue
                line_match = MEMINFO_LINE.match(line)
                if not line_match:
                    continue
                key = line_match.group(1).lower()
                if key in MEMINFO_TITLES or self.verbose:
                    value = long(line_match.group(2))
                    properties[key] = value

        return properties

    def __instrument_meminfo_path(self, job_directory):
        return self._instrument_file_path(job_directory, 'meminfo')


__all__ = ('MemInfoPlugin', )