# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\InputTailAction.py
# Compiled at: 2017-03-23 05:01:21
# Size of source mod 2**32: 2834 bytes
"""
TailAction.py
-------------

Copyright 2016 Davide Mastromatteo
"""
import datetime, os.path, re, tyler
from flows.Actions.Action import Action

class TailAction(Action):
    __doc__ = '\n    TailAction Class\n    '
    type = 'tail'

    def on_init(self):
        super().on_init()
        self.path = self.configuration['input']
        self.buffer = []
        self.timeout = 3
        self.last_flush_date = datetime.datetime.now()
        self.file_is_opened = False
        self.regex = ''
        self.my_log_file = None
        self.enable_buffer = False
        if 'regex_new_buffer' in self.configuration:
            self.regex = self.configuration['regex_new_buffer']
            self.enable_buffer = True
        if 'timeout' in self.configuration:
            self.timeout = int(self.configuration['regex_new_buffer'])
        self.try_opening_file()

    def try_opening_file(self):
        """Try to open the input file"""
        if os.path.isfile(self.path):
            self.my_log_file = tyler.Tyler(self.path)
            try:
                for line in self.my_log_file:
                    pass

            except StopIteration:
                pass

            self.file_is_opened = True

    def bufferize_line(self, line):
        """ Insert a new line into the buffer """
        self.buffer.append(line)

    def flush_buffer(self):
        """ Flush the buffer of the tail """
        if len(self.buffer) > 0:
            return_value = ''.join(self.buffer)
            self.buffer.clear()
            self.send_message(return_value)
            self.last_flush_date = datetime.datetime.now()

    def on_cycle(self):
        super().on_cycle()
        for line in self.my_log_file:
            if not self.enable_buffer:
                self.send_message(line)
                return
            match = re.search(self.regex, line)
            if match is None:
                self.bufferize_line(line)
                return
            self.flush_buffer()
            self.bufferize_line(line)

        if (datetime.datetime.now() - self.last_flush_date).total_seconds() > self.timeout:
            self.flush_buffer()