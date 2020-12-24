# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pirx/checks.py
# Compiled at: 2013-12-04 20:00:46
import socket, sys

def host(name):
    return socket.gethostname() == name


def arg(name, value=None):
    args = [ arg.split('=') for arg in sys.argv[1:] ]
    for arg in args:
        if arg[0].lsplit('--') == name:
            if len(arg) > 1:
                return arg[1] == value
            else:
                return True