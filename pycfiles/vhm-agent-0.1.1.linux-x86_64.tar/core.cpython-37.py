# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pavelstudenik/Develop/vhm-manager/venv/lib/python3.7/site-packages/vhmlib/core.py
# Compiled at: 2020-04-03 16:20:39
# Size of source mod 2**32: 247 bytes
import subprocess

class Command:

    @staticmethod
    def execute(params):
        command = subprocess.run(params, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), text=True)
        return (command.returncode, command.stdout or command.stderr)