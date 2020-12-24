# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/apptool/cli.py
# Compiled at: 2010-10-09 01:07:17
import os, sys, backup, restore

class Color:
    bold = '\x1b[1;1m'
    green = '\x1b[1;32m'
    cyan = '\x1b[1;36m'
    yellow = '\x1b[1;33m'
    red = '\x1b[1;31m'
    off = '\x1b[1;0m'


def usage():
    usage = '\n    usage: apptool {backup|restore}\n\n    backup    Backup Apps\n    restore   Restore Apps\n    help      This help\n          '
    print usage


def success(msg):
    if os.name == 'nt':
        print msg
    else:
        print Color.cyan + '==> ' + Color.off + Color.bold + msg + Color.off


def message(msg):
    if os.name == 'nt':
        print msg
    else:
        print Color.green + '==> ' + Color.off + Color.bold + msg + Color.off


def warning(msg):
    if os.name == 'nt':
        print msg
    else:
        print Color.yellow + '==> ' + Color.off + Color.bold + msg + Color.off


def error(err):
    if os.name == 'nt':
        print >> sys.stderr, err
    else:
        print >> sys.stderr, Color.red + '==> ' + Color.off + Color.bold + err + Color.off
    sys.exit(1)


def parseArgs(argv):
    if len(argv) < 2:
        return error('Not enough arguments')
    else:
        if len(argv) > 2:
            return error('Too many arguments')
        if argv[1] == 'help':
            return usage()
        if argv[1] == 'backup':
            return backup.backupApps()
        if argv[1] == 'restore':
            return restore.restoreApps()
        return error("`%s' not recognized" % argv[1])