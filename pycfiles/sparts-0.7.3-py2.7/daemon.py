# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sparts/daemon.py
# Compiled at: 2015-01-08 02:58:40
"""This module defines helpers for running and managing daemonized services"""
from __future__ import absolute_import
import errno, logging, os, signal
from sparts.deps import HAS_DAEMONIZE
from sparts.fileutils import readfile
if HAS_DAEMONIZE:
    from daemonize import Daemonize

def _using_pidfile(pidfile, logger):
    """Log what `pidfile` we'll be using to `logger`"""
    logger.info("Using lockfile at '%s'...", pidfile)


def read_pid(pidfile, logger):
    """Returns the pid in `pidfile` or None if the file doesn't exist."""
    _using_pidfile(pidfile, logger)
    try:
        return int(readfile(pidfile))
    except IOError as e:
        if e.errno == errno.ENOENT:
            logger.info('Daemon not running (no lockfile)')
            return
        raise

    return


def send_signal(pid, signum, logger):
    """Sends signal `signum` to `pid`, logging messages to `logger`"""
    logger.info('Sending signal %d to PID %d...', signum, pid)
    os.kill(pid, signum)


def daemonize(command, name, pidfile, logger, **kwargs):
    """Daemonizes the `command` function.
    
    Uses `name` for syslogging, `pidfile` for the pid file, and logs messages
    to `logger` or a child logger of logger as appropriate.
    """
    if not HAS_DAEMONIZE:
        raise Exception('Need `daemonize` to run as daemon')
    _using_pidfile(pidfile, logger)
    daemon = Daemonize(app=name, pid=pidfile, action=command, logger=logging.getLogger(logger.name + '.daemon'), **kwargs)
    daemon.start()


def kill(pidfile, logger, signum=signal.SIGTERM):
    """Sends `signum` to the pid specified by `pidfile`.

    Logs messages to `logger`.  Returns True if the process is not running,
    or signal was sent successfully.  Returns False if the process for the
    pidfile was running and there was an error sending the signal."""
    daemon_pid = read_pid(pidfile, logger)
    if daemon_pid is None:
        return True
    else:
        try:
            send_signal(daemon_pid, signum, logger)
            return True
        except OSError as e:
            if e.errno == errno.ESRCH:
                logger.warning('Daemon not running (Stale lockfile)')
                os.remove(pidfile)
                return True
            if e.errno == errno.EPERM:
                logger.error('Unable to kill %d (EPERM)', daemon_pid)
                return False
            raise

        return


def status(pidfile, logger):
    """Checks to see if the process for the pid in `pidfile` is running.

    Logs messages to `logger`.  Returns True if there is a program for the
    running pid.  Returns False if not or if there was an error
    polling the pid."""
    daemon_pid = read_pid(pidfile, logger)
    if daemon_pid is None:
        return False
    else:
        try:
            send_signal(daemon_pid, 0, logger)
            logger.info('Daemon is alive')
            return True
        except OSError as e:
            if e.errno == errno.ESRCH:
                logger.warning('Daemon not running (Stale lockfile)')
                os.remove(pidfile)
                return False
            if e.errno == errno.EPERM:
                logger.error('Unable to poll %d (EPERM)', daemon_pid)
                return False
            raise

        return