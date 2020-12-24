# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/phenry/.config/i3/fluidspaces/src/fluidspaces/rofi_commands.py
# Compiled at: 2017-10-23 03:12:01
# Size of source mod 2**32: 498 bytes
import subprocess

class RofiCommands(object):

    @staticmethod
    def menu(choices_str, prompt='Select workspace: '):
        """Display Rofi menu of choices and return the one the user picks (or None)"""
        proc = subprocess.Popen([
         'rofi', '-dmenu', '-p', prompt],
          stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE))
        chosen_str = proc.communicate(choices_str)[0].decode('utf-8').strip()
        if chosen_str:
            return chosen_str