# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tkpip\lib\dist.py
# Compiled at: 2013-08-24 12:07:58
from __future__ import division, absolute_import, print_function, unicode_literals
import logging
from pkg_resources import load_entry_point
install_func = load_entry_point(b'pip', b'console_scripts', b'pip')

def dist_install(name):
    print((b'Installing {0}').format(name))
    try:
        args = [b'install',
         name]
        res = install_func(args)
        print((b'Finished ({0})!').format(res))
    except Exception as e:
        logging.exception(e)


def dist_upgrade(name):
    print((b'Upgrading {0}').format(name))
    try:
        args = [b'install',
         b'--upgrade',
         name]
        res = install_func(args)
        print((b'Finished ({0})!').format(res))
    except Exception as e:
        logging.exception(e)


def dist_uninstall(name, dist=None):
    if dist:
        name += b'==' + dist.version
    print((b'Uninstalling {0}').format(name))
    try:
        args = [b'uninstall',
         b'-y',
         name]
        res = install_func(args)
        print((b'Finished ({0})!').format(res))
    except Exception as e:
        logging.exception(e)