# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/titan/monitors.py
# Compiled at: 2014-10-17 04:08:03
from __future__ import unicode_literals
import getpass, datetime
from os import stat, environ
from sys import exit
from glob import glob
from pwd import getpwuid
from shutil import rmtree
from os.path import isdir, join, sep
from titan.tools.system import shell_out
import urllib2, urllib, httplib, json
from config import titanConfig
TITAN_PATH = environ.get(b'TITAN_PATH') or b'/var/lib/titan/'
TITAN_CONFIG = join(b'/etc/', b'titan.conf')
CONFIG = titanConfig(TITAN_CONFIG, TITAN_PATH)
MONITOR_PATH = CONFIG[b'main'][b'monitorstore']

def install(args):
    PREFIX = b'[ Monitor::Install ] '
    if does_monitor_exist(args[0]):
        print PREFIX, b'This monitor already exists'
        exit(2)
    print PREFIX, b'Locating monitor: %s' % args[0]
    if validate_repo(args[0]):
        print PREFIX, b"Found monitor: '%s'" % args[0].rsplit(b'/', 1)[1].split(b'.')[0]
        shell_out(b'cd %s && sudo git clone %s' % (MONITOR_PATH, args[0]))
        shell_out(b'sudo chown -R _titanosx %s' % MONITOR_PATH)
        if does_monitor_exist(args[0]):
            print PREFIX, b'Monitor successfully installed'
        else:
            print PREFIX, b'There was an error installing the monitor'
    else:
        print PREFIX, b'That is not a valid module, not installing anything'
        exit(1)


def upgrade(args):
    PREFIX = b'[ Monitor::Upgrade ] '
    if does_monitor_exist(args[0]):
        print PREFIX, b'Upgrading %s' % args[0]
        result = shell_out(b'cd %s && sudo git stash && sudo git fetch && sudo git diff FETCH_HEAD && sudo git pull -f' % join(MONITOR_PATH, args[0]))
        print PREFIX, result
        print PREFIX, b'Done'
    else:
        print PREFIX, b'This is not installed'
        exit(1)


def remove(args):
    PREFIX = b'[ Monitor::Remove ] '
    if getpass.getuser() != b'root':
        print PREFIX, b'Please run this with elevated permissions'
        exit(1)
    if does_monitor_exist(args[0]):
        monitor_path = join(MONITOR_PATH, args[0])
        owner = find_owner(monitor_path)
        if b'_titanosx' != owner:
            print PREFIX, b'Unable to remove, invalid permissions'
            exit(128)
        else:
            rmtree(monitor_path)
        if does_monitor_exist(args[0]):
            print PREFIX, b'Removing monitor failed'
        else:
            print PREFIX, b'Successfully remove monitor'
    else:
        print PREFIX, b"Could not find a monitor by the name of '%s'" % args[0]
        exit(1)


def list(args):
    print b'The following titanOSX monitors are installed:\n'
    monitors = [ monitor for monitor in glob(join(MONITOR_PATH, b'*')) if monitor.find(b'README.md') is -1 ]
    if len(monitors) == 0:
        print b'None'
        exit()
    for monitor in monitors:
        stats = stat(monitor)
        monitor_name = monitor.rsplit(b'/', 1)[1]
        install_date = datetime.datetime.fromtimestamp(int(stats.st_mtime)).strftime(b'%d-%b %y @ %H:%M:%S')
        sourced_from = shell_out(b'git -C %s remote -v' % monitor)
        print (b'{}\n\tInstalled on: {}\n\tSourced From:   {}').format(monitor_name, install_date, sourced_from.replace(b'\n', b'\n\t\t\t'))


def does_monitor_exist(monitor):
    monitor = monitor.rsplit(b'/', 1)[(-1)].split(b'.')[0]
    if isdir(join(MONITOR_PATH, monitor)):
        return True
    else:
        return False


def find_owner(filename):
    return getpwuid(stat(filename).st_uid).pw_name


def validate_repo(target):
    result = shell_out(b'git ls-remote %s' % target)
    if b'HEAD' in result:
        return True
    return False