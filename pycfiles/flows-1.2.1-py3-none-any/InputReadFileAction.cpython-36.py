# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\InputReadFileAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 1197 bytes
"""
ReadFileAction.py
-----------------

Copyright 2016 Davide Mastromatteo
"""
import os.path
from flows.Actions.Action import Action

class ReadFileAction(Action):
    __doc__ = '\n    ReadFileAction Class\n    '
    type = 'readfile'
    path = ''
    file = None
    file_is_opened = False
    offset_file_name = ''

    def on_init(self):
        super().on_init()
        self.path = self.configuration['input']
        self.try_opening_file()

    def try_opening_file(self):
        """Try to open the input file"""
        if os.path.isfile(self.path):
            self.file = open(self.path, 'r')
            self.file_is_opened = True

    def on_stop(self):
        super().on_stop()
        if os.path.isfile(self.offset_file_name):
            os.remove(self.offset_file_name)

    def on_cycle(self):
        super().on_cycle()
        if not self.file_is_opened:
            self.try_opening_file()
        line = self.file.readline()
        if len(line) == 0:
            self.file.close()
            return
        self.send_message(line)