# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/wangping/svn/work/code/project/AntShell/lib/antshell/utils/parser.py
# Compiled at: 2019-10-21 23:26:39
# Size of source mod 2**32: 4539 bytes
from __future__ import absolute_import, division, print_function
from antshell.utils.release import __prog__, __version__, __banner__
from utils.lang import LANG
from antshell.config import CONFIG
import sys, argparse

def load_argParser():
    """command line parameter"""
    langset = CONFIG.DEFAULT.LANGSET
    lang = LANG[langset]
    usage = "%(prog)s [ -h | --version ] [-l [-m 2] ]\n        [ v | -n 1 | -s 'ip|name' ] [ -A ] [ -B ] \n        [ -e | -d | -a ip [--name tag | --user root | --passwd *** | --port 22 | --sudo root ] ]\n        "
    version = '%(prog)s ' + __version__
    parser = argparse.ArgumentParser(prog=__prog__,
      usage=usage,
      description=(lang['desc']),
      add_help=False)
    parser.add_argument('v', nargs='?', help=('%s' % lang['v']))
    g1 = parser.add_argument_group('system arguments')
    g1.add_argument('-h', '--help', action='help', help=(lang['help']))
    g1.add_argument('--version', action='version', version=version, help=(lang['version']))
    g1.add_argument('--init', dest='init', action='store_true', default=False, help=(lang['init']))
    g2 = parser.add_argument_group('host arguments')
    g2.add_argument('-a', '--add', dest='add', action='store', type=str, help=(lang['add']), metavar='ip')
    g2.add_argument('-e', '--edit', dest='edit', action='store_true', default=False, help=(lang['edit']))
    g2.add_argument('-d', '--delete', dest='delete', action='store_true', default=False, help=(lang['delete']))
    g2.add_argument('--name', dest='name', action='store', type=str, help=(lang['name']), default='', metavar='name')
    g2.add_argument('--user', dest='user', action='store', type=str, help=(lang['user']), default='', metavar='root')
    g2.add_argument('--passwd', dest='passwd', action='store', type=str, help=(lang['passwd']), default='', metavar='******')
    g2.add_argument('--port', dest='port', action='store', type=int, help=(lang['port']), default=0, metavar='22')
    g2.add_argument('--sudo', dest='sudo', action='store', type=str, help=(lang['sudo']), default='', metavar='root')
    g3 = parser.add_argument_group('manager arguments')
    g3.add_argument('-l', dest='list', action='store_true', default=False, help=(lang['list']))
    g3.add_argument('-m', '--mode', dest='mode', action='store', type=int, help=(lang['mode']), default=0, metavar='2')
    g3.add_argument('-n', dest='num', action='store', type=int, help=(lang['num']), metavar=0)
    g3.add_argument('-s', '--search', dest='search', action='store', type=str, help=(lang['search']), default='', metavar="'ip|name'")
    g3.add_argument('-A', '--agent', dest='agent', action='store_true', default=False, help=(lang['agent']))
    g3.add_argument('-B', '--bastion', dest='bastion', action='store_true', default=False, help=(lang['bastion']))
    g3.add_argument('-E', '--engine', dest='engine', action='store', type=str, help=(lang['engine']), default='', metavar="'expect|paramiko'")
    return parser