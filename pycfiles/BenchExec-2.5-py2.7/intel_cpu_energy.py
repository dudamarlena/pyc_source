# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/intel_cpu_energy.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import collections, logging, os, subprocess, signal, re
from benchexec.util import find_executable
from decimal import Decimal
DOMAIN_PACKAGE = b'package'
DOMAIN_CORE = b'core'
DOMAIN_UNCORE = b'uncore'
DOMAIN_DRAM = b'dram'

class EnergyMeasurement(object):

    def __init__(self, executable):
        self._executable = executable
        self._measurement_process = None
        return

    @classmethod
    def create_if_supported(cls):
        executable = find_executable(b'cpu-energy-meter', exitOnError=False, use_current_dir=False)
        if executable is None:
            logging.debug(b'Energy measurement not available because cpu-energy-meter binary could not be found.')
            return
        else:
            return cls(executable)

    def start(self):
        """Starts the external measurement program."""
        assert not self.is_running(), b'Attempted to start an energy measurement while one was already running.'
        self._measurement_process = subprocess.Popen([
         self._executable, b'-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10000, preexec_fn=os.setpgrp)

    def stop(self):
        """Stops the external measurement program and returns the measurement result,
        if the measurement was running."""
        consumed_energy = collections.defaultdict(dict)
        if not self.is_running():
            return
        else:
            self._measurement_process.send_signal(signal.SIGINT)
            out, err = self._measurement_process.communicate()
            assert self._measurement_process.returncode is not None
            if self._measurement_process.returncode:
                logging.debug(b'Energy measurement terminated with return code %s', self._measurement_process.returncode)
            self._measurement_process = None
            for line in err.splitlines():
                logging.debug(b'energy measurement stderr: %s', line)

            for line in out.splitlines():
                line = line.decode(b'ASCII')
                logging.debug(b'energy measurement output: %s', line)
                match = re.match(b'cpu(\\d+)_([a-z]+)_joules=(\\d+\\.?\\d*)', line)
                if not match:
                    continue
                cpu, domain, energy = match.groups()
                cpu = int(cpu)
                energy = Decimal(energy)
                consumed_energy[cpu][domain] = energy

            return consumed_energy

    def is_running(self):
        """Returns True if there is currently an instance of the external measurement program running, False otherwise."""
        return self._measurement_process is not None


def format_energy_results(energy):
    """Take the result of an energy measurement and return a flat dictionary that contains all values."""
    if not energy:
        return {}
    result = {}
    cpuenergy = Decimal(0)
    for pkg, domains in energy.items():
        for domain, value in domains.items():
            if domain == DOMAIN_PACKAGE:
                cpuenergy += value
                result[(b'cpuenergy-pkg{}').format(pkg)] = value
            else:
                result[(b'cpuenergy-pkg{}-{}').format(pkg, domain)] = value

    result[b'cpuenergy'] = cpuenergy
    result = collections.OrderedDict(sorted(result.items()))
    return result