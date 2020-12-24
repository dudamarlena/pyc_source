# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/__init__.py
# Compiled at: 2020-03-20 08:07:41
# Size of source mod 2**32: 808 bytes
__doc__ = 'pwclip init module'
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