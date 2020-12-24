# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/systeminfo.py
# Compiled at: 2019-11-28 13:06:28
"""
This module allows to retrieve information about the current system.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import glob, logging, os, platform, sys
from benchexec import util
__all__ = [
 b'has_swap',
 b'is_turbo_boost_enabled',
 b'CPUThrottleCheck',
 b'SystemInfo',
 b'SwapCheck']
_TURBO_BOOST_FILE = b'/sys/devices/system/cpu/cpufreq/boost'
_TURBO_BOOST_FILE_PSTATE = b'/sys/devices/system/cpu/intel_pstate/no_turbo'

class SystemInfo(object):

    def __init__(self):
        """
        This function finds some information about the computer.
        """
        self.hostname = platform.node()
        self.os = platform.platform(aliased=True)
        cpuInfo = dict()
        self.cpu_max_frequency = b'unknown'
        cpuInfoFilename = b'/proc/cpuinfo'
        self.cpu_number_of_cores = b'unknown'
        if os.path.isfile(cpuInfoFilename) and os.access(cpuInfoFilename, os.R_OK):
            cpuInfoFile = open(cpuInfoFilename, b'rt')
            cpuInfoLines = [ tuple(line.split(b':')) for line in cpuInfoFile.read().replace(b'\n\n', b'\n').replace(b'\t', b'').strip(b'\n').split(b'\n')
                           ]
            cpuInfo = dict(cpuInfoLines)
            cpuInfoFile.close()
            self.cpu_number_of_cores = str(len([ line for line in cpuInfoLines if line[0] == b'processor' ]))
        self.cpu_model = cpuInfo.get(b'model name', b'unknown').strip().replace(b'(R)', b'').replace(b'(TM)', b'').replace(b'(tm)', b'')
        if b'cpu MHz' in cpuInfo:
            self.cpu_max_frequency = int(float(cpuInfo[b'cpu MHz'])) * 1000 * 1000
        freqInfoFilename = b'/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_max_freq'
        if os.path.isfile(freqInfoFilename) and os.access(freqInfoFilename, os.R_OK):
            frequencyInfoFile = open(freqInfoFilename, b'rt')
            cpu_max_frequency = frequencyInfoFile.read().strip(b'\n')
            frequencyInfoFile.close()
            self.cpu_max_frequency = int(cpu_max_frequency) * 1000
        self.cpu_turboboost = is_turbo_boost_enabled()
        memInfo = dict()
        memInfoFilename = b'/proc/meminfo'
        if os.path.isfile(memInfoFilename) and os.access(memInfoFilename, os.R_OK):
            memInfoFile = open(memInfoFilename, b'rt')
            memInfo = dict(tuple(s.split(b': ')) for s in memInfoFile.read().replace(b'\t', b'').strip(b'\n').split(b'\n'))
            memInfoFile.close()
        self.memory = memInfo.get(b'MemTotal', b'unknown').strip()
        if self.memory.endswith(b' kB'):
            self.memory = int(self.memory[:-3]) * 1024
        self.environment = os.environ.copy()
        self.environment.pop(b'HOME', None)
        self.environment.pop(b'TMPDIR', None)
        self.environment.pop(b'TMP', None)
        self.environment.pop(b'TEMPDIR', None)
        self.environment.pop(b'TEMP', None)
        return


class CPUThrottleCheck(object):
    """
    Class for checking whether the CPU has throttled during some time period.
    """

    def __init__(self, cores=None):
        """
        Create an instance that monitors the given list of cores (or all CPUs).
        """
        self.cpu_throttle_count = {}
        cpu_pattern = (b'[{0}]').format((b',').join(map(str, cores))) if cores else b'*'
        for file in glob.glob((b'/sys/devices/system/cpu/cpu{}/thermal_throttle/*_throttle_count').format(cpu_pattern)):
            try:
                self.cpu_throttle_count[file] = int(util.read_file(file))
            except Exception as e:
                logging.warning(b'Cannot read throttling count of CPU from kernel: %s', e)

    def has_throttled(self):
        """
        Check whether any of the CPU cores monitored by this instance has
        throttled since this instance was created.
        @return a boolean value
        """
        for file, value in self.cpu_throttle_count.items():
            try:
                new_value = int(util.read_file(file))
                if new_value > value:
                    return True
            except Exception as e:
                logging.warning(b'Cannot read throttling count of CPU from kernel: %s', e)

        return False


class SwapCheck(object):
    """
    Class for checking whether the system has swapped during some period.
    """

    def __init__(self):
        self.swap_count = self._read_swap_count()

    def _read_swap_count(self):
        try:
            return {k:int(v) for k, v in util.read_key_value_pairs_from_file(b'/proc/vmstat') if k in ('pswpin',
                                                                                                       'pswpout') if k in ('pswpin',
                                                                                                                           'pswpout')}
        except Exception as e:
            logging.warning(b'Cannot read swap count from kernel: %s', e)

    def has_swapped(self):
        """
        Check whether any swapping occured on this system since this instance was created.
        @return a boolean value
        """
        new_values = self._read_swap_count()
        for key, new_value in new_values.items():
            old_value = self.swap_count.get(key, 0)
            if new_value > old_value:
                return True

        return False


def is_turbo_boost_enabled():
    """
    Check whether Turbo Boost (scaling CPU frequency beyond nominal frequency)
    is active on this system.
    @return: A bool, or None if Turbo Boost is not supported.
    """
    try:
        if os.path.exists(_TURBO_BOOST_FILE):
            boost_enabled = int(util.read_file(_TURBO_BOOST_FILE))
            if not 0 <= boost_enabled <= 1:
                raise ValueError((b'Invalid value {} for turbo boost activation').format(boost_enabled))
            return boost_enabled != 0
        if os.path.exists(_TURBO_BOOST_FILE_PSTATE):
            boost_disabled = int(util.read_file(_TURBO_BOOST_FILE_PSTATE))
            if not 0 <= boost_disabled <= 1:
                raise ValueError((b'Invalid value {} for turbo boost activation').format(boost_enabled))
            return boost_disabled != 1
    except ValueError as e:
        sys.exit((b'Could not read turbo-boost information from kernel: {0}').format(e))


def has_swap():
    with open(b'/proc/meminfo', b'r') as (meminfo):
        for line in meminfo:
            if line.startswith(b'SwapTotal:'):
                swap = line.split()[1]
                if int(swap) == 0:
                    return False

    return True