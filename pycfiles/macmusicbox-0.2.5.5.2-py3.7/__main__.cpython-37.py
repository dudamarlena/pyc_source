# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/NEMbox/__main__.py
# Compiled at: 2020-03-16 06:17:15
# Size of source mod 2**32: 1177 bytes
"""
网易云音乐 Entry
"""
from __future__ import print_function, unicode_literals, division, absolute_import
import curses, traceback, argparse, sys
from future.builtins import str
from .menu import Menu
from .__version__ import __version__ as version

def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version',
      help='show this version and exit',
      action='store_true')
    args = parser.parse_args()
    if args.version:
        latest = Menu().check_version()
        curses.endwin()
        print('NetEase-MusicBox installed version:' + version)
        if latest != version:
            print('NetEase-MusicBox latest version:' + str(latest))
        sys.exit()
    nembox_menu = Menu()
    try:
        nembox_menu.start_fork(version)
    except (OSError, TypeError, ValueError, KeyError, IndexError):
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()


if __name__ == '__main__':
    start()