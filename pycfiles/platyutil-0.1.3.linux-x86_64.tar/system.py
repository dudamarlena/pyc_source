# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/platyutil/system.py
# Compiled at: 2016-03-16 05:10:54
import os, logging, select, fcntl
from os import path
from subprocess import Popen, PIPE, CalledProcessError

def ensureDirectory(dirpath):
    """Ensure the existance of the given dir path."""
    if not path.isdir(dirpath):
        os.makedirs(dirpath)


def mount(dev, mountpoint, flags='', log=None):
    """Mount the given dev to the given mountpoint by using the given flags"""
    ensureDirectory(mountpoint)
    systemCall('mount %s %s %s' % (flags, dev, mountpoint), log=log)


def umount(mountpoint, flags='', log=None):
    """Unmount given mountpoint."""
    systemCall('umount %s %s' % (flags, mountpoint), log=log)


def systemCall(cmd, sh=True, log=None):
    """Fancy magic version of os.system"""
    if log is None:
        log = logging
    log.debug('System call [sh:%s]: %s' % (
     sh, cmd))
    out = []
    proc = None
    poller = None
    outBuf = ['']
    errBuf = ['']

    def pollOutput():
        """
        Read, log and store output (if any) from processes pipes.
        """
        removeChars = '\r\n'
        fds = [ entry[0] for entry in poller.poll() ]
        if proc.stdout.fileno() in fds:
            while True:
                try:
                    tmp = proc.stdout.read(100)
                except IOError:
                    break

                outBuf[0] += tmp
                while '\n' in outBuf[0]:
                    line, _, outBuf[0] = outBuf[0].partition('\n')
                    log.debug(line)
                    out.append(line + '\n')

                if not tmp:
                    break

        if proc.stderr.fileno() in fds:
            while True:
                try:
                    tmp = proc.stderr.read(100)
                except IOError:
                    break

                errBuf[0] += tmp
                while '\n' in errBuf[0]:
                    line, _, errBuf[0] = errBuf[0].partition('\n')
                    log.warning(line)

                if not tmp:
                    break

    while True:
        if proc is None:
            proc = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=sh)
            poller = select.poll()
            flags = fcntl.fcntl(proc.stdout, fcntl.F_GETFL)
            fcntl.fcntl(proc.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            flags = fcntl.fcntl(proc.stderr, fcntl.F_GETFL)
            fcntl.fcntl(proc.stderr, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            poller.register(proc.stdout, select.POLLIN)
            poller.register(proc.stderr, select.POLLIN)
        pollOutput()
        if proc.poll() is not None:
            break

    pollOutput()
    if proc.returncode != 0:
        raise RuntimeError(CalledProcessError(proc.returncode, cmd, ('').join(out)))
    return ('').join(out)


def chrootedSystemCall(chrootDir, cmd, sh=True, mountPseudoFs=True, log=None):
    """Chrooted version of systemCall. Manages necessary pseudo filesystems."""
    if log is None:
        log = conduct.app.log
    proc = path.join(chrootDir, 'proc')
    sys = path.join(chrootDir, 'sys')
    dev = path.join(chrootDir, 'dev')
    devpts = path.join(chrootDir, 'dev', 'pts')
    if mountPseudoFs:
        mount('proc', proc, '-t proc')
        mount('/sys', sys, '--rbind')
        mount('/dev', dev, '--rbind')
    try:
        log.debug('Execute chrooted command ...')
        cmd = 'chroot %s %s' % (chrootDir, cmd)
        return systemCall(cmd, sh, log)
    finally:
        if mountPseudoFs:
            if path.exists(devpts):
                umount(devpts, '-lf')
            umount(dev, '-lf')
            umount(sys, '-lf')
            umount(proc, '-lf')

    return