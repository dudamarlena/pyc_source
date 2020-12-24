# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/charlagui/utils/parser.py
# Compiled at: 2019-09-11 09:48:28
# Size of source mod 2**32: 2281 bytes
import os, glob
from io import StringIO
import json

class Parser:

    def __init__(self):
        self.current_settings = {}

    def parse_2_dict(self):
        for file in glob.iglob('*/**.kts'):
            with open(os.path.realpath(file), 'r') as (file):
                for root, dirs, files in os.walk('./'):
                    for file2 in files:
                        if file2.endswith('.kts') and file2 in file.name:
                            filename = file2.replace('.kts', '').lower()

                self.current_settings.update({str(filename): {}})
                lines = file.readlines()
                settings_dict = {}
                for line in lines:
                    if 'import' not in line and '*' not in line:
                        split_lines = line.split(' ')
                        if split_lines[0] != '\n':
                            settings_dict.update({split_lines[0]: ' '.join(split_lines[2:])})

                self.current_settings[str(filename)] = settings_dict

        return 'Settings Parse Complete'

    def update_settings(self, setting, settings_obj):
        self.current_settings[setting] = settings_obj
        self.save_to_file(setting)

    def save_to_file(self, setting):
        for file in glob.iglob('*/**.kts'):
            if setting in file.lower():
                with open(os.path.realpath(file), 'w') as (file1):
                    write_str = 'import com.charlatano.settings.*\n'
                    if 'ESP' in file:
                        write_str += 'import com.charlatano.game.Color\n'
                    if 'BunnyHop' in file:
                        write_str += 'import java.awt.event.KeyEvent\n'
                    if 'Advanced' in file:
                        write_str += 'import com.sun.jna.platform.win32.WinNT\n'
                    for k, v in self.current_settings[setting].items():
                        value = v
                        if not v.endswith('\n'):
                            value += '\n'
                        write_str += str(k + ' = ' + value)

                    file1.write(write_str)