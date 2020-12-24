# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\pip_install.py
# Compiled at: 2020-05-05 06:57:08
# Size of source mod 2**32: 260 bytes
from os import *

def install(s):
    system('python -m pip install ' + s + '>pip_install.log')


def uninstall(s):
    system('python -m pip unstall ' + s + '>pip_uninstall.log')


def upgrade(s):
    system('python -m pip install --upgrade ' + s + '>pip_upgrade.log')