# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phenry/.config/i3/fluidspaces/src/fluidspaces/menu_commands.py
# Compiled at: 2017-10-25 04:10:39
# Size of source mod 2**32: 430 bytes
import subprocess

class MenuCommands(object):

    @staticmethod
    def menu(command, choices_str):
        """Display menu of choices and return the one the user picks (or None)"""
        proc = subprocess.Popen(command, stdin=(subprocess.PIPE), stdout=(subprocess.PIPE))
        stdout, stderr = proc.communicate(choices_str)
        chosen_str = stdout.decode('utf-8').strip()
        if chosen_str:
            return chosen_str