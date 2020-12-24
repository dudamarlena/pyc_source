# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enthys/workspace/python/python_commander/venv/lib/python3.5/site-packages/python_commander/py_commander.py
# Compiled at: 2018-10-31 08:00:25
# Size of source mod 2**32: 113 bytes
from . import Commander

def commander_start():
    Commander.gather_commands()
    Commander.execute_commands()