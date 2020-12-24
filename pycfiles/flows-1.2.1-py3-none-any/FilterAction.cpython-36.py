# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\Users\mastromatteo\Progetti\flows\flows\Actions\FilterAction.py
# Compiled at: 2017-03-23 05:01:20
# Size of source mod 2**32: 2320 bytes
"""
FilterAction.py
----------------------------

Copyright 2016 Davide Mastromatteo
"""
import re, os
from flows.Actions.Action import Action

class FilterAction(Action):
    __doc__ = '\n    FilterAction Class\n    '
    type = 'filter'
    regex = ''
    regexes_file = ''
    ignorecase = False
    invert_match = False
    regexes = []

    def on_init(self):
        super().on_init()
        self.regexes = []
        if 'regexes_file' in self.configuration:
            self.regexes_file = self.configuration['regexes_file']
            if os.path.isfile(self.regexes_file):
                file_containing_regexes = open(self.regexes_file)
                self.regexes = file_containing_regexes.readlines()
                file_containing_regexes.close()
            else:
                print(self.regexes_file + ' not found, skipped')
        if 'regex' in self.configuration:
            self.regexes.append(self.configuration['regex'])
        if 'subtype' in self.configuration:
            subtype = self.configuration['subtype']
            if subtype == 'invert':
                self.invert_match = True
        if 'ignorecase' in self.configuration:
            self.ignorecase = True

    def on_input_received(self, action_input=None):
        super().on_input_received(action_input)
        return_value = action_input.message
        flags = 0
        if self.ignorecase:
            flags = re.IGNORECASE
        else:
            if not self.invert_match:
                for regex in self.regexes:
                    regex = regex.strip()
                    if regex != '':
                        match = re.search(regex, action_input.message, flags)
                        if match is not None:
                            self.send_message(return_value)

            else:
                for regex in self.regexes:
                    regex = regex.strip()
                    match = re.search(regex, action_input.message, flags)
                    if match is not None:
                        return

                self.send_message(return_value)