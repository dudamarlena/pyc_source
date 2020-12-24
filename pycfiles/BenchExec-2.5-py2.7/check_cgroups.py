# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/check_cgroups.py
# Compiled at: 2019-11-28 13:06:28
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse, logging, os, sys, tempfile, threading
sys.dont_write_bytecode = True
from benchexec.cgroups import *
from benchexec.runexecutor import RunExecutor
from benchexec import util

def check_cgroup_availability(wait=1):
    """
    Basic utility to check the availability and permissions of cgroups.
    This will log some warnings for the user if necessary.
    On some systems, daemons such as cgrulesengd might interfere with the cgroups
    of a process soon after it was started. Thus this function starts a process,
    waits a configurable amount of time, and check whether the cgroups have been changed.
    @param wait: a non-negative int that is interpreted as seconds to wait during the check
    @raise SystemExit: if cgroups are not usable
    """
    logging.basicConfig(format=b'%(levelname)s: %(message)s')
    runexecutor = RunExecutor(use_namespaces=False)
    my_cgroups = runexecutor.cgroups
    if not (CPUACCT in my_cgroups and CPUSET in my_cgroups and MEMORY in my_cgroups):
        sys.exit(1)
    with tempfile.NamedTemporaryFile(mode=b'rt') as (tmp):
        runexecutor.execute_run([
         b'sh', b'-c', (b'sleep {0}; cat /proc/self/cgroup').format(wait)], tmp.name, memlimit=1048576, cores=util.parse_int_list(my_cgroups.get_value(CPUSET, b'cpus')), memory_nodes=my_cgroups.read_allowed_memory_banks())
        lines = []
        for line in tmp:
            line = line.strip()
            if line and not line == (b"sh -c 'sleep {0}; cat /proc/self/cgroup'").format(wait) and not all(c == b'-' for c in line):
                lines.append(line)

    task_cgroups = find_my_cgroups(lines)
    fail = False
    for subsystem in (CPUACCT, CPUSET, MEMORY, FREEZER):
        if subsystem in my_cgroups:
            if not task_cgroups[subsystem].startswith(os.path.join(my_cgroups[subsystem], b'benchmark_')):
                logging.warning(b'Task was in cgroup %s for subsystem %s, which is not the expected sub-cgroup of %s. Maybe some other program is interfering with cgroup management?', task_cgroups[subsystem], subsystem, my_cgroups[subsystem])
                fail = True

    if fail:
        sys.exit(1)


def check_cgroup_availability_in_thread(options):
    """
    Run check_cgroup_availability() in a separate thread to detect the following problem:
    If "cgexec --sticky" is used to tell cgrulesengd to not interfere
    with our child processes, the sticky flag unfortunately works only
    for processes spawned by the main thread, not those spawned by other threads
    (and this will happen if "benchexec -N" is used).
    """
    thread = _CheckCgroupsThread(options)
    thread.start()
    thread.join()
    if thread.error:
        raise thread.error


class _CheckCgroupsThread(threading.Thread):
    error = None

    def __init__(self, options):
        super(_CheckCgroupsThread, self).__init__()
        self.options = options

    def run(self):
        try:
            check_cgroup_availability(self.options.wait)
        except BaseException as e:
            self.error = e


def main(argv=None):
    """
    A simple command-line interface for the cgroups check of BenchExec.
    """
    if argv is None:
        argv = sys.argv
    parser = argparse.ArgumentParser(fromfile_prefix_chars=b'@', description=b'Check whether cgroups are available and can be used for BenchExec.\n           Part of BenchExec: https://github.com/sosy-lab/benchexec/')
    parser.add_argument(b'--wait', type=int, default=1, metavar=b'SECONDS', help=b'wait some time to ensure no process interferes with cgroups in the meantime (default: 1s)')
    parser.add_argument(b'--no-thread', action=b'store_true', help=b'run check on the main thread instead of a separate thread' + b'(behavior of cgrulesengd differs depending on this)')
    options = parser.parse_args(argv[1:])
    if options.no_thread:
        check_cgroup_availability(options.wait)
    else:
        check_cgroup_availability_in_thread(options)
    return


if __name__ == b'__main__':
    main()