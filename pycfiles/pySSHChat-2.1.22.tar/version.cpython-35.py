# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vlad/source/pySSHChat/pysshchat/version.py
# Compiled at: 2018-03-31 12:17:54
# Size of source mod 2**32: 436 bytes
import subprocess
from os.path import isdir, join, dirname
PREFIX = '1.0.%s'

def get_version():
    d = dirname(__file__)
    if isdir('.git'):
        version = PREFIX % int(subprocess.check_output(['git', 'rev-list', '--all', '--count']))
        with open(join(d, '.version'), 'w') as (f):
            f.write(version)
    else:
        with open(join(d, '.version'), 'r') as (f):
            version = f.read()
    return version