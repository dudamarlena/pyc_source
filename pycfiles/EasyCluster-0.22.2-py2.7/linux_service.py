# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easycluster/linux_service.py
# Compiled at: 2019-04-18 17:28:18
from __future__ import print_function
import sys, os, signal, subprocess, traceback, time, easycluster as _core
if _core.PYTHON3:
    NAME = 'EasyCluster-Py3'
    SUFFIX = '-py3'
else:
    NAME = 'EasyCluster'
    SUFFIX = ''
MODULE = 'easycluster'
MAIN_MODULE = MODULE + '.__main__'
PIDFILE = '/var/run/easycluster%s.pid' % SUFFIX
KEY_PATH = '/etc/easycluster_service%s.key' % SUFFIX
INIT_PATH = '/etc/init.d/easycluster%s' % SUFFIX
SERVICE_NAME = 'easycluster%s' % SUFFIX
INIT_SCRIPT = '#!/bin/sh\n# chkconfig: 345 99 01\n# description: EasyCluster remote service\n# processname: easycluster%(suffix)s\n\n### BEGIN INIT INFO\n# Provides:          easycluster%(suffix)s\n# Required-Start:    $remote_fs $syslog\n# Required-Stop:     $remote_fs $syslog\n# Default-Start:     2 3 4 5\n# Default-Stop:      0 1 6\n# Short-Description: Control the EasyCluster service.\n### END INIT INFO\n\n# Author: J. K. Stafford <jspenguin@jspenguin.org>\n\nPATH=/sbin:/usr/sbin:/bin:/usr/bin\n\nexec \'%(exe)s\' -m %(name)s "$@"\n'

def install_service():
    temp_path = INIT_PATH + '~'
    with open(temp_path, 'w') as (fp):
        fp.write(INIT_SCRIPT % dict(exe=sys.executable, name=__name__, suffix=SUFFIX))
    os.chmod(temp_path, 493)
    os.rename(temp_path, INIT_PATH)
    for prog in (['update-rc.d', SERVICE_NAME, 'defaults'],
     [
      'chkconfig', '--add', SERVICE_NAME],
     [
      '/usr/lib/lsb/install_initd', SERVICE_NAME]):
        try:
            subprocess.call(prog)
        except OSError:
            pass
        else:
            break

    else:
        raise OSError('No method of installing initscripts found (tried Debian, Redhat, LSB)')


def uninstall_service():
    for prog in (['update-rc.d', '-f', SERVICE_NAME, 'remove'],
     [
      'chkconfig', '--del', SERVICE_NAME],
     [
      '/usr/lib/lsb/remove_initd', SERVICE_NAME]):
        try:
            subprocess.call(prog)
        except OSError:
            pass
        else:
            break

    else:
        raise OSError('No method of uninstalling initscripts found (tried Debian, Redhat, LSB)')

    try:
        os.unlink(INIT_PATH)
    except (IOError, OSError):
        pass

    return 0


def start_service():
    return start_daemon()


def stop_service():
    return stop_daemon()


def query_service_installed():
    return os.path.exists(INIT_PATH)


def is_daemon(pid, name):
    try:
        os.kill(pid, 0)
    except OSError:
        return False

    try:
        cmdf = '/proc/%d/cmdline' % pid
        if not os.path.exists(cmdf):
            return True
        with open(cmdf, 'r') as (fp):
            cmdline = fp.read().split('\x00')
        if cmdline[1] == '-m' and cmdline[2] == name:
            return True
    except (EnvironmentError, ValueError):
        pass

    return False


def read_pidfile(fil):
    try:
        with open(fil, 'r') as (fp):
            return int(fp.read().strip())
    except (EnvironmentError, ValueError):
        return 0


def getpid():
    pid = read_pidfile(PIDFILE)
    if not pid:
        return
    if not is_daemon(pid, MAIN_MODULE):
        try:
            os.unlink(PIDFILE)
        except Exception:
            pass

        return 0
    return pid


def start_daemon():
    opid = getpid()
    if opid:
        print('%s is already running.' % NAME)
        return 1
    print('Starting %s: ' % NAME, end='')
    exitstat = subprocess.call([sys.executable, '-m', MAIN_MODULE, '-S', '-k', KEY_PATH, '-d', '-P', PIDFILE])
    if exitstat:
        print('failed.')
        return 2
    print('ok.')
    return 0


def stop_daemon():
    pid = getpid()
    if not pid:
        print('%s is not running.' % NAME)
        return 1
    try:
        print('Stopping %s: ' % NAME, end='')
        os.kill(pid, signal.SIGTERM)
        try:
            os.unlink(PIDFILE)
        except Exception:
            pass

        print('success.')
        return 0
    except Exception:
        print('failed.')
        return 2


def init_main():
    exitstat = 0
    cmd = sys.argv[1]
    if cmd == 'start':
        exitstat = start_daemon()
    elif cmd == 'stop':
        exitstat = stop_daemon()
    elif cmd == 'reload' or cmd == 'force-reload':
        pid = getpid()
        if pid:
            os.kill(pid, signal.SIGHUP)
            exitstat = 1
        else:
            print('%s is not running.' % NAME)
    elif cmd == 'status':
        pid = getpid()
        if pid:
            print('%s is running.' % NAME)
        else:
            exitstat = 1
            print('%s is not running.' % NAME)
    elif cmd == 'restart':
        stop_daemon()
        time.sleep(2)
        exitstat = start_daemon()
    else:
        print('Usage: %s {start|stop|restart|reload|force-reload}' % sys.argv[0], file=sys.stderr)
        exitstat = 1
    return exitstat


if __name__ == '__main__':
    sys.exit(init_main())