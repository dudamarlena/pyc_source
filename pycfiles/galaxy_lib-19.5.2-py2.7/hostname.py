# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/jobs/metrics/instrumenters/hostname.py
# Compiled at: 2018-09-15 08:40:24
"""The module describes the ``cpuinfo`` job metrics plugin."""
import logging
from . import InstrumentPlugin
from .. import formatting
log = logging.getLogger(__name__)

class HostnameFormatter(formatting.JobMetricFormatter):

    def format(self, key, value):
        return (
         key, value)


class HostnamePlugin(InstrumentPlugin):
    """ Gather hostname
    """
    plugin_type = 'hostname'
    formatter = HostnameFormatter()

    def __init__(self, **kwargs):
        pass

    def pre_execute_instrument(self, job_directory):
        return "hostname -f > '%s'" % self.__instrument_hostname_path(job_directory)

    def job_properties(self, job_id, job_directory):
        with open(self.__instrument_hostname_path(job_directory)) as (f):
            return {'hostname': f.read().strip()}

    def __instrument_hostname_path(self, job_directory):
        return self._instrument_file_path(job_directory, 'hostname')


__all__ = ('HostnamePlugin', )