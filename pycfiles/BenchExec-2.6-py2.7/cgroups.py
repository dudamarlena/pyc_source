# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benchexec/cgroups.py
# Compiled at: 2020-05-07 05:52:35
from __future__ import absolute_import, division, print_function, unicode_literals
import logging, os, shutil, signal, tempfile, time
from benchexec import util
__all__ = [
 b'find_my_cgroups',
 b'find_cgroups_of_process',
 b'BLKIO',
 b'CPUACCT',
 b'CPUSET',
 b'FREEZER',
 b'MEMORY']
CGROUP_FALLBACK_PATH = b'system.slice/benchexec-cgroup.service'
CGROUP_NAME_PREFIX = b'benchmark_'
BLKIO = b'blkio'
CPUACCT = b'cpuacct'
CPUSET = b'cpuset'
FREEZER = b'freezer'
MEMORY = b'memory'
ALL_KNOWN_SUBSYSTEMS = {
 BLKIO,
 CPUACCT,
 CPUSET,
 FREEZER,
 MEMORY,
 b'cpu',
 b'devices',
 b'net_cls',
 b'net_prio',
 b'hugetlb',
 b'perf_event',
 b'pids'}

def find_my_cgroups(cgroup_paths=None):
    """
    Return a Cgroup object with the cgroups of the current process.
    Note that it is not guaranteed that all subsystems are available
    in the returned object, as a subsystem may not be mounted.
    Check with "subsystem in <instance>" before using.
    A subsystem may also be present but we do not have the rights to create
    child cgroups, this can be checked with require_subsystem().
    @param cgroup_paths: If given, use this instead of reading /proc/self/cgroup.
    """
    logging.debug(b'Analyzing /proc/mounts and /proc/self/cgroup for determining cgroups.')
    if cgroup_paths is None:
        my_cgroups = dict(_find_own_cgroups())
    else:
        my_cgroups = dict(_parse_proc_pid_cgroup(cgroup_paths))
    cgroupsParents = {}
    for subsystem, mount in _find_cgroup_mounts():
        if os.access(mount, os.F_OK):
            cgroupPath = os.path.join(mount, my_cgroups[subsystem])
            if not os.access(cgroupPath, os.W_OK) and os.access(os.path.join(cgroupPath, CGROUP_FALLBACK_PATH), os.W_OK):
                cgroupPath = os.path.join(cgroupPath, CGROUP_FALLBACK_PATH)
            cgroupsParents[subsystem] = cgroupPath

    return Cgroup(cgroupsParents)


def find_cgroups_of_process(pid):
    """
    Return a Cgroup object that represents the cgroups of a given process.
    """
    with open((b'/proc/{}/cgroup').format(pid), b'rt') as (cgroups_file):
        return find_my_cgroups(cgroups_file)


def _find_cgroup_mounts():
    """
    Return the information which subsystems are mounted where.
    @return a generator of tuples (subsystem, mountpoint)
    """
    try:
        with open(b'/proc/mounts', b'rt') as (mountsFile):
            for mount in mountsFile:
                mount = mount.split(b' ')
                if mount[2] == b'cgroup':
                    mountpoint = mount[1]
                    options = mount[3]
                    for option in options.split(b','):
                        if option in ALL_KNOWN_SUBSYSTEMS:
                            yield (
                             option, mountpoint)

    except IOError:
        logging.exception(b'Cannot read /proc/mounts')


def _find_own_cgroups():
    """
    For all subsystems, return the information in which (sub-)cgroup this process is in.
    (Each process is in exactly cgroup in each hierarchy.)
    @return a generator of tuples (subsystem, cgroup)
    """
    try:
        with open(b'/proc/self/cgroup', b'rt') as (ownCgroupsFile):
            for cgroup in _parse_proc_pid_cgroup(ownCgroupsFile):
                yield cgroup

    except IOError:
        logging.exception(b'Cannot read /proc/self/cgroup')


def _parse_proc_pid_cgroup(content):
    """
    Parse a /proc/*/cgroup file into tuples of (subsystem,cgroup).
    @param content: An iterable over the lines of the file.
    @return: a generator of tuples
    """
    for ownCgroup in content:
        ownCgroup = ownCgroup.strip().split(b':')
        try:
            path = ownCgroup[2][1:]
        except IndexError:
            raise IndexError(b'index out of range for ' + str(ownCgroup))

        for subsystem in ownCgroup[1].split(b','):
            yield (
             subsystem, path)


def kill_all_tasks_in_cgroup(cgroup, ensure_empty=True):
    tasksFile = os.path.join(cgroup, b'tasks')
    i = 0
    while True:
        i += 1
        for sig in [signal.SIGKILL, signal.SIGINT, signal.SIGTERM]:
            with open(tasksFile, b'rt') as (tasks):
                task = None
                for task in tasks:
                    task = task.strip()
                    if i > 1:
                        logging.warning(b'Run has left-over process with pid %s in cgroup %s, sending signal %s (try %s).', task, cgroup, sig, i)
                    util.kill_process(int(task), sig)

                if task is None or not ensure_empty:
                    return
            time.sleep(i * 0.5)

    return


def remove_cgroup(cgroup):
    if not os.path.exists(cgroup):
        logging.warning(b'Cannot remove CGroup %s, because it does not exist.', cgroup)
        return
    assert os.path.getsize(os.path.join(cgroup, b'tasks')) == 0
    try:
        os.rmdir(cgroup)
    except OSError:
        try:
            os.rmdir(cgroup)
        except OSError as e:
            logging.warning(b'Failed to remove cgroup %s: error %s (%s)', cgroup, e.errno, e.strerror)


def _register_process_with_cgrulesengd(pid):
    """Tell cgrulesengd daemon to not move the given process into other cgroups,
    if libcgroup is available.
    """
    from ctypes import cdll
    try:
        libcgroup = cdll.LoadLibrary(b'libcgroup.so.1')
        failure = libcgroup.cgroup_init()
        if failure:
            pass
        else:
            CGROUP_DAEMON_UNCHANGE_CHILDREN = 1
            failure = libcgroup.cgroup_register_unchanged_process(pid, CGROUP_DAEMON_UNCHANGE_CHILDREN)
            if failure:
                pass
    except OSError:
        pass


class Cgroup(object):

    def __init__(self, cgroupsPerSubsystem):
        assert set(cgroupsPerSubsystem.keys()) <= ALL_KNOWN_SUBSYSTEMS
        assert all(cgroupsPerSubsystem.values())
        self.per_subsystem = cgroupsPerSubsystem
        self.paths = set(cgroupsPerSubsystem.values())

    def __contains__(self, key):
        return key in self.per_subsystem

    def __getitem__(self, key):
        return self.per_subsystem[key]

    def __str__(self):
        return str(self.paths)

    def require_subsystem(self, subsystem, log_method=logging.warning):
        """
        Check whether the given subsystem is enabled and is writable
        (i.e., new cgroups can be created for it).
        Produces a log message for the user if one of the conditions is not fulfilled.
        If the subsystem is enabled but not writable, it will be removed from
        this instance such that further checks with "in" will return "False".
        @return A boolean value.
        """
        if subsystem not in self:
            log_method(b'Cgroup subsystem %s is not enabled. Please enable it with "sudo mount -t cgroup none /sys/fs/cgroup".', subsystem)
            return False
        try:
            test_cgroup = self.create_fresh_child_cgroup(subsystem)
            test_cgroup.remove()
        except OSError as e:
            self.paths = set(self.per_subsystem.values())
            log_method((b'Cannot use cgroup hierarchy mounted at {0} for subsystem {1}, reason: {2}. If permissions are wrong, please run "sudo chmod o+wt \'{0}\'".').format(self.per_subsystem[subsystem], subsystem, e.strerror))
            del self.per_subsystem[subsystem]
            return False

        return True

    def create_fresh_child_cgroup(self, *subsystems):
        """
        Create child cgroups of the current cgroup for at least the given subsystems.
        @return: A Cgroup instance representing the new child cgroup(s).
        """
        assert set(subsystems).issubset(self.per_subsystem.keys())
        createdCgroupsPerSubsystem = {}
        createdCgroupsPerParent = {}
        for subsystem in subsystems:
            parentCgroup = self.per_subsystem[subsystem]
            if parentCgroup in createdCgroupsPerParent:
                createdCgroupsPerSubsystem[subsystem] = createdCgroupsPerParent[parentCgroup]
                continue
            cgroup = tempfile.mkdtemp(prefix=CGROUP_NAME_PREFIX, dir=parentCgroup)
            createdCgroupsPerSubsystem[subsystem] = cgroup
            createdCgroupsPerParent[parentCgroup] = cgroup

            def copy_parent_to_child(name):
                shutil.copyfile(os.path.join(parentCgroup, name), os.path.join(cgroup, name))

            try:
                copy_parent_to_child(b'cpuset.cpus')
                copy_parent_to_child(b'cpuset.mems')
            except IOError:
                pass

        return Cgroup(createdCgroupsPerSubsystem)

    def add_task(self, pid):
        """
        Add a process to the cgroups represented by this instance.
        """
        _register_process_with_cgrulesengd(pid)
        for cgroup in self.paths:
            with open(os.path.join(cgroup, b'tasks'), b'w') as (tasksFile):
                tasksFile.write(str(pid))

    def get_all_tasks(self, subsystem):
        """
        Return a generator of all PIDs currently in this cgroup for the given subsystem.
        """
        with open(os.path.join(self.per_subsystem[subsystem], b'tasks'), b'r') as (tasksFile):
            for line in tasksFile:
                yield int(line)

    def kill_all_tasks(self):
        """
        Kill all tasks in this cgroup and all its children cgroups forcefully.
        Additionally, the children cgroups will be deleted.
        """

        def kill_all_tasks_in_cgroup_recursively(cgroup, delete):
            for dirpath, dirs, files in os.walk(cgroup, topdown=False):
                for subCgroup in dirs:
                    subCgroup = os.path.join(dirpath, subCgroup)
                    kill_all_tasks_in_cgroup(subCgroup, ensure_empty=delete)
                    if delete:
                        remove_cgroup(subCgroup)

            kill_all_tasks_in_cgroup(cgroup, ensure_empty=delete)

        if FREEZER in self.per_subsystem:
            cgroup = self.per_subsystem[FREEZER]
            freezer_file = os.path.join(cgroup, b'freezer.state')
            util.write_file(b'FROZEN', freezer_file)
            kill_all_tasks_in_cgroup_recursively(cgroup, delete=False)
            util.write_file(b'THAWED', freezer_file)
        for cgroup in self.paths:
            kill_all_tasks_in_cgroup_recursively(cgroup, delete=True)

    def has_value(self, subsystem, option):
        """
        Check whether the given value exists in the given subsystem.
        Does not make a difference whether the value is readable, writable, or both.
        Do not include the subsystem name in the option name.
        Only call this method if the given subsystem is available.
        """
        assert subsystem in self
        return os.path.isfile(os.path.join(self.per_subsystem[subsystem], subsystem + b'.' + option))

    def get_value(self, subsystem, option):
        """
        Read the given value from the given subsystem.
        Do not include the subsystem name in the option name.
        Only call this method if the given subsystem is available.
        """
        assert subsystem in self, (b'Subsystem {} is missing').format(subsystem)
        return util.read_file(self.per_subsystem[subsystem], subsystem + b'.' + option)

    def get_file_lines(self, subsystem, option):
        """
        Read the lines of the given file from the given subsystem.
        Do not include the subsystem name in the option name.
        Only call this method if the given subsystem is available.
        """
        assert subsystem in self
        with open(os.path.join(self.per_subsystem[subsystem], subsystem + b'.' + option)) as (f):
            for line in f:
                yield line

    def get_key_value_pairs(self, subsystem, filename):
        """
        Read the lines of the given file from the given subsystem
        and split the lines into key-value pairs.
        Do not include the subsystem name in the option name.
        Only call this method if the given subsystem is available.
        """
        assert subsystem in self
        return util.read_key_value_pairs_from_file(self.per_subsystem[subsystem], subsystem + b'.' + filename)

    def set_value(self, subsystem, option, value):
        """
        Write the given value for the given subsystem.
        Do not include the subsystem name in the option name.
        Only call this method if the given subsystem is available.
        """
        assert subsystem in self
        util.write_file(str(value), self.per_subsystem[subsystem], subsystem + b'.' + option)

    def remove(self):
        """
        Remove all cgroups this instance represents from the system.
        This instance is afterwards not usable anymore!
        """
        for cgroup in self.paths:
            remove_cgroup(cgroup)

        del self.paths
        del self.per_subsystem

    def read_cputime(self):
        """
        Read the cputime usage of this cgroup. CPUACCT cgroup needs to be available.
        @return cputime usage in seconds
        """
        return float(self.get_value(CPUACCT, b'usage')) / 1000000000

    def read_allowed_memory_banks(self):
        """Get the list of all memory banks allowed by this cgroup."""
        return util.parse_int_list(self.get_value(CPUSET, b'mems'))