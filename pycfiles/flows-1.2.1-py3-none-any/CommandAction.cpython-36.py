# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\CommandAction.py
# Compiled at: 2017-03-23 05:01:14
# Size of source mod 2**32: 2130 bytes
"""
CommandAction.py
----------------

Copyright 2016 Davide Mastromatteo
License: Apache-2.0
"""
import time, subprocess
from flows.Actions.Action import Action

class CommandAction(Action):
    __doc__ = '\n    CommandAction Class\n    '
    type = 'command'
    command = ''

    def on_init(self):
        super().on_init()
        if 'command' not in self.configuration:
            raise ValueError(str.format('The command action {0} is not properly configured:The command parameter is missing', self.name))
        self.command = self.configuration['command']

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        input_message = action_input.message
        cmd = self.command
        cmd = cmd.replace('{input}', input_message)
        cmd = cmd.replace('{date}', time.strftime('%d/%m/%Y'))
        cmd = cmd.replace('{time}', time.strftime('%H:%M:%S'))
        if action_input.file_system_event is not None:
            cmd = cmd.replace('{event_type}', action_input.file_system_event.event_type)
            cmd = cmd.replace('{file_source}', action_input.file_system_event.src_path)
            cmd = cmd.replace('{is_directory}', str(action_input.file_system_event.is_directory))
            if hasattr(action_input.file_system_event, 'dest_path'):
                cmd = cmd.replace('{file_destination}', action_input.file_system_event.src_path)
        process = subprocess.run(cmd, shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT),
          universal_newlines=True)
        out = process.stdout
        output_string = str(out.strip().encode('ascii', 'ignore').decode('utf-8'))
        self.send_message(output_string)