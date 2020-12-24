# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/__init__.py
# Compiled at: 2020-03-20 08:07:41
# Size of source mod 2**32: 808 bytes
"""pwclip init module"""
import sys
from os import path, devnull, environ, getenv, remove, name as osname
__lib = path.join(path.dirname(__file__), 'lib')
if path.exists(__lib):
    if __lib not in sys.path:
        sys.path = [
         __lib] + sys.path
if sys.platform == 'win32':
    if sys.executable.split('\\')[(-1)] == 'pythonw.exe':
        sys.stdout = open(devnull, 'w')
        sys.stderr = open(devnull, 'w')
from pwclip.cmdline import cli, gui

def pwclip():
    """pwclip passcrypt gui mode"""
    gui()


def ykclip():
    """pwclip yubico gui mode"""
    gui('yk')


def pwcli():
    """pwclip cli mode"""
    cli()