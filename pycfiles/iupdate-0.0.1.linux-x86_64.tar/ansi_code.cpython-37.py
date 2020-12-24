# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/iupdate/lib/ansi_code.py
# Compiled at: 2019-10-15 02:40:23
# Size of source mod 2**32: 709 bytes


class AnsiCode:

    def __init__(self):
        self.warning = '\x1b[0;93m⚠ '
        self.error = '\x1b[0;91m✖ '
        self.finish = '\x1b[0;92m✔ '
        self.reply = '\x1b[0;95m→ '
        self.header = '\x1b[0;95m '
        self.reset = '\x1b[0m'

    def message(self, function, style, message, jumpline='\n'):
        if function == 'print':
            return print(f"{style}{message}{self.reset}")
        if function == 'input':
            try:
                return input(f"{style}{message}{jumpline}>> {self.reset}")
            except KeyboardInterrupt:
                print(f"{jumpline}{self.warning}Aborted by user.{self.reset}")