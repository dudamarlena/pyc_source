# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/Framework/Utils/print_Utils.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 5443 bytes
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
import sys, traceback
from warrior.WarriorCore.Classes.war_print_class import print_main

def print_debug(message, *args):
    """Print a debug message to the terminal """
    print_type = '-D-'
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    print_main(message, print_type)
    return message


def print_notype(message, *args):
    """Prints with out print type(-I-,-E-),with color cyan in bold TEXT """
    print_type = ''
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    color_message = None
    if sys.stdout.isatty():
        color_message = '\x1b[0;34m' + str(message) + '\x1b[0m '
    print_main(message, print_type, color_message)
    return message


def print_normal(message, *args):
    """Prints with out print type(-I-,-E-),with color cyan in bold TEXT """
    print_type = ''
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    print_main(message, print_type)
    return message


def print_without_logging(message, *args):
    """Prints without writing to log file"""
    print_type = '-N-'
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    print_main(message, print_type, logging=False)
    return message


def print_info(message, *args):
    """Print an info message to the terminal """
    print_type = '-I-'
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    color_message = None
    if sys.stdout.isatty():
        msg_upper = message.upper()
        if ':PASS' in msg_upper:
            color_message = message[:msg_upper.index(':PASS') + 1] + '\x1b[1;32m' + 'PASS' + '\x1b[0m' + message[msg_upper.index(':PASS') + 5:]
        else:
            if ':RAN' in msg_upper:
                color_message = message[:msg_upper.index(':RAN') + 1] + '\x1b[1;32m' + 'RAN' + '\x1b[0m' + message[msg_upper.index(':RAN') + 5:]
            else:
                if ':FAIL' in msg_upper:
                    color_message = message[:msg_upper.index(':FAIL') + 1] + '\x1b[1;31m' + 'FAIL' + '\x1b[0m' + message[msg_upper.index(':FAIL') + 5:]
                else:
                    if ':EXCEPTION' in msg_upper:
                        color_message = message[:msg_upper.index(':EXCEPTION') + 1] + '\x1b[1;31m' + 'EXCEPTION' + '\x1b[0m' + message[msg_upper.index(':EXCEPTION') + 10:]
                    else:
                        if ':ERROR' in msg_upper:
                            color_message = message[:msg_upper.index(':ERROR') + 1] + '\x1b[1;31m' + 'ERROR' + '\x1b[0m' + message[msg_upper.index(':ERROR') + 6:]
                        elif ':SKIPPED' in msg_upper:
                            color_message = message[:msg_upper.index(':SKIPPED') + 1] + '\x1b[1;33m' + 'SKIPPED' + '\x1b[0m' + message[msg_upper.index(':SKIPPED') + 9:]
    print_main(message, print_type, color_message)
    return message


def print_error(message, *args):
    """Prints an error message to the terminal """
    print_type = '-E-'
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    color_message = None
    if sys.stdout.isatty():
        print_type = '\x1b[1;31m-E-\x1b[0m'
        color_message = '\x1b[1;31m' + str(message) + '\x1b[0m'
    print_main(message, print_type, color_message)
    return message


def print_exception(exception):
    """Print details of an exception to the console """
    print_info('\n')
    print_error('!!! *** Exception occurred during execution *** !!!')
    print_error('Exception Name: {0}'.format(exception.__class__.__name__))
    print_error('Exception trace back: \n \t{0}'.format(traceback.format_exc()))
    return traceback.format_exc()


def print_warning(message, *args):
    """Prints a warning message to the terminal """
    print_type = '-W-'
    if len(args) > 0:
        for arg in args:
            message += arg + ', '

    color_message = None
    if sys.stdout.isatty():
        print_type = '\x1b[1;33m-W-\x1b[0m'
        color_message = '\x1b[1;33m' + str(message) + '\x1b[0m'
    print_main(message, print_type, color_message)
    return message


def print_sub(message, *args):
    """Substitutes the string with *args tuple provided
    User has to provide the place holder for substitution in the message
    as {0}, {1}, {2} ..etc and the corresponding values in the *args.

    Eg: print_sub("My name is {0} {1}, I live in {2}", 'John', 'Doe', 'Texas')
    Output: My Name is John Doe, I live in Texas
    """
    print_type = '-I-'
    message = (message.format)(*args)
    print_main(message, print_type)
    return message