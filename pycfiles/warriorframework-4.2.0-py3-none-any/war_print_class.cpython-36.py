# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/Classes/war_print_class.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 3774 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import sys, re

def print_main(message, print_type, color_message=None, *args, **kwargs):
    """The main print function will be called by other print functions
    """
    if color_message is not None:
        print_string = print_type + ' ' + str(color_message)
    else:
        if color_message is None:
            print_string = print_type + ' ' + str(message)
        else:
            if args:
                print_string = print_type + ' ' + str(message) + str(args)
            if isinstance(sys.stdout, RedirectPrint):
                sys.stdout.write((print_string + '\n'), logging=(kwargs.get('logging', True)))
            else:
                sys.stdout.write(print_string + '\n')
        sys.stdout.flush()
        from warrior.Framework.Utils.testcase_Utils import TCOBJ
        if TCOBJ.pnote is False:
            TCOBJ.p_note_level(message, print_type)
    return print_string


class RedirectPrint(object):
    __doc__ = 'Class that has methods to redirect prints\n    from stdout to correct console log files '

    def __init__(self, console_logfile):
        """Constructor"""
        self.get_file(console_logfile)
        self.stdout = sys.stdout
        self.console_full_log = None
        self.console_add = None
        self.katana_obj = None

    def katana_console_log(self, katana_obj):
        """
            set the console log object to be the katana communcation object
        """
        self.console_full_log = katana_obj['console_full_log']
        self.console_add = katana_obj['console_add']
        self.katana_obj = katana_obj

    def get_file(self, console_logfile):
        """If the console logfile is not None redirect sys.stdout to
        console logfile
        """
        self.file = console_logfile
        if self.file is not None:
            sys.stdout = self

    def write(self, data, logging=True):
        """
        - Writes data to the sys.stdout
        - Writes data to log file only if the logging is True
        - Removes the ansii escape chars before writing to file
        """
        self.stdout.write(data)
        ansi_escape = re.compile('\\x1b[^m]*m')
        data = ansi_escape.sub('', data)
        if logging is True:
            self.file.write(data)
            self.file.flush()
        if self.katana_obj is not None:
            if 'console_full_log' in self.katana_obj:
                if 'console_add' in self.katana_obj:
                    self.katana_obj['console_full_log'] += data
                    self.katana_obj['console_add'] += data

    def isatty(self):
        """Check if sys.stdout is a tty """
        return self.stdout.isatty()

    def flush(self):
        """flush logfile """
        return self.stdout.flush()