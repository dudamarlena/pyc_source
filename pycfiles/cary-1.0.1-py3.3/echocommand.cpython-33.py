# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cary/echocommand.py
# Compiled at: 2015-08-04 06:07:13
# Size of source mod 2**32: 1366 bytes
from cary.carycommand import CaryCommand, CaryAction
import os

class EchoCommand(CaryCommand):

    @property
    def name(self):
        return 'echo'

    @property
    def description(self):
        return 'Echo the body and attachments of a message back to the sender'

    @property
    def required_attachments(self):
        return ['any']

    def _create_action(self, parsed_message):
        return EchoAction(parsed_message)


class EchoAction(CaryAction):

    def __init__(self, parsed_message):
        super().__init__(parsed_message)

    def validate_command(self):
        """
        The echo command always succeeds.
        """
        self.command_is_valid = True

    def execute_action(self):
        self._output_filenames = []
        for attachment in self._attachments:
            stub = os.path.split(attachment)[(-1)]
            output_filename = os.path.join(self.output_dir, stub)
            with open(attachment) as (fin):
                with open(output_filename, 'w') as (fout):
                    fout.write(fin.read())
                    self._output_filenames.append(output_filename)

    @property
    def response_subject(self):
        return 'echo echo'

    @property
    def response_body(self):
        return 'Echoed:\n\n' + self._message.body