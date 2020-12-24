# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vermeul/openbis/obis/src/python/obis/dm/command_log.py
# Compiled at: 2019-05-21 15:45:31
# Size of source mod 2**32: 2040 bytes
from datetime import datetime
import os

class CommandLog(object):
    __doc__ = ' CommandLog can write a log for a command with multiple steps.\n    The idea is that, when a later step fails, we want to know what happened \n    before. This can be useful for cases where no automatic recovery can \n    be done. If the success method is called, the log is removed.\n    If there is an existing log, the user must first make sure everything \n    is in order and delete the log before using obis '

    def __init__(self):
        self.folder_path = os.path.join(os.path.expanduser('~'), '.obis', 'log')
        self.file_paths = []
        self.logs = []
        self.most_recent_command = None

    def any_log_exists(self):
        if os.path.exists(self.folder_path) == False:
            return False
        else:
            return len(os.listdir(self.folder_path)) != 0

    def log(self, command, message):
        self.logs.append((command, message))
        if len(self.logs) == 1:
            return
        if len(self.logs) == 2:
            first_command, first_message = self.logs[0]
            self._log(first_command, first_message)
        self._log(command, message)

    def log_error(self, error):
        if self.most_recent_command is not None:
            self._log(self.most_recent_command, error)

    def _log(self, command, message):
        self.most_recent_command = command
        if os.path.exists(self.folder_path) == False:
            os.makedirs(self.folder_path)
        file_path = os.path.join(self.folder_path, command + '.log')
        self.file_paths.append(file_path)
        timestamp = datetime.now().strftime('%H:%M:%S')
        with open(file_path, 'a') as (file):
            file.write(timestamp + ': ' + message + '\n')

    def success(self):
        for file_path in self.file_paths:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.rmdir(self.folder_path)