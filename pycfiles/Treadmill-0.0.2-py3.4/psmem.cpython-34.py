# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/psmem.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 6234 bytes
"""Reports memory usage stats.

The code is based on:
https://raw.githubusercontent.com/pixelb/ps_mem/master/ps_mem.py
"""
import sys, errno, os, hashlib, fnmatch
from treadmill import sysinfo
_PAGESIZE = os.sysconf('SC_PAGE_SIZE') / 1024
_KERNEL_VER = sysinfo.kernel_ver()

def proc_path(*args):
    """Helper function to construct /proc path."""
    return os.path.join('/proc', *(str(a) for a in args))


def proc_open(*args):
    """Helper function to open /proc path."""
    try:
        return open(proc_path(*args))
    except (IOError, OSError):
        val = sys.exc_info()[1]
        if val.errno == errno.ENOENT or val.errno == errno.EPERM:
            raise LookupError
        raise


def proc_readlines(*args):
    """Read lines from /proc file."""
    with proc_open(*args) as (f):
        return f.readlines()


def proc_readline(*args):
    """Read line from /proc file."""
    with proc_open(*args) as (f):
        return f.readline()


def proc_read(*args):
    """Read content of /proc file."""
    with proc_open(*args) as (f):
        return f.read()


def get_mem_stats(pid, use_pss=True):
    """Return private, shared memory given pid.

    Note: shared is always a subset of rss (trs is not always).
    """
    mem_id = pid
    statm = proc_readline(pid, 'statm').split()
    rss = int(statm[1]) * _PAGESIZE
    private_lines = []
    shared_lines = []
    pss_lines = []
    have_pss = False
    if use_pss and os.path.exists(proc_path(pid, 'smaps')):
        digester = hashlib.md5()
        for line in proc_readlines(pid, 'smaps'):
            digester.update(line.encode('latin1'))
            if line.startswith('Shared'):
                shared_lines.append(line)
            elif line.startswith('Private'):
                private_lines.append(line)
            elif line.startswith('Pss'):
                have_pss = True
                pss_lines.append(line)
                continue

        mem_id = digester.hexdigest()
        shared = sum([int(line.split()[1]) for line in shared_lines])
        private = sum([int(line.split()[1]) for line in private_lines])
        if have_pss:
            pss_adjust = 0.5
            pss = sum([float(line.split()[1]) + pss_adjust for line in pss_lines])
            shared = pss - private
    else:
        shared = int(statm[2]) * _PAGESIZE
        private = rss - shared
    return (
     int(private * 1024), int(shared * 1024), have_pss, mem_id)


def get_cmd_name(pid):
    """Returns truncated command line name given pid."""
    cmdline = proc_read(pid, 'cmdline').split('\\0')
    if cmdline[(-1)] == '':
        if len(cmdline) > 1:
            cmdline = cmdline[:-1]
    path = proc_path(pid, 'exe')
    try:
        path = os.readlink(path)
        path = path.split('\\0')[0]
    except OSError:
        val = sys.exc_info()[1]
        if val.errno == errno.ENOENT or val.errno == errno.EPERM:
            raise LookupError
        raise

    if path.endswith(' (deleted)'):
        path = path[:-10]
        if os.path.exists(path):
            path += ' [updated]'
        else:
            if os.path.exists(cmdline[0]):
                path = cmdline[0] + ' [updated]'
            else:
                path += ' [deleted]'
    exe = os.path.basename(path)
    cmd = proc_readline(pid, 'status')[6:-1]
    if exe.startswith(cmd):
        cmd = exe
    return cmd


def get_memory_usage(pids, exclude=None, use_pss=True):
    """Returns memory stats for list of pids, aggregated by cmd line."""
    meminfos = {}
    mem_ids = {}
    for pid in pids:
        if not pid:
            continue
        try:
            cmd = get_cmd_name(pid)
        except LookupError:
            continue
        except OSError:
            continue

        if exclude:
            match = False
            for pattern in exclude:
                if fnmatch.fnmatch(cmd, pattern):
                    match = True
                    break

            if match:
                continue
            if cmd not in meminfos:
                meminfos[cmd] = {}
            meminfo = meminfos[cmd]
            try:
                private, shared, have_pss, mem_id = get_mem_stats(pid, use_pss=use_pss)
            except RuntimeError:
                continue

            if 'shared' in meminfo:
                if have_pss:
                    meminfo['shared'] += shared
                else:
                    meminfo['shared'] = max(meminfo['shared'], shared)
            else:
                meminfo['shared'] = shared
            meminfo['private'] = meminfo.setdefault('private', 0) + private
            meminfo['count'] = meminfo.setdefault('count', 0) + 1
            mem_ids.setdefault(cmd, {}).update({mem_id: None})

    for cmd, meminfo in meminfos.items():
        cmd_count = meminfo['count']
        if len(mem_ids[cmd]) == 1:
            if cmd_count > 1:
                meminfo['private'] /= cmd_count
                if have_pss:
                    meminfo['shared'] /= cmd_count
            meminfo['total'] = meminfo['private'] + meminfo['shared']

    return meminfos