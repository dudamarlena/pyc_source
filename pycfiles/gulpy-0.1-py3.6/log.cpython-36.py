# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\gulpy\log.py
# Compiled at: 2017-01-14 11:48:31
# Size of source mod 2**32: 2653 bytes
"""Module responsible to print formatted outputs.

>>> from gulpy import log
>>> log('TaskName', 'LOG')
[0:00:00](TaskName): LOG

"""
import ctypes, os
from datetime import datetime
from multiprocessing import freeze_support
if os.name == 'nt':
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
start_time = datetime.now()
colors = {'green':'\x1b[92m', 
 'yellow':'\x1b[93m', 
 'cyan':'\x1b[96m', 
 'blue':'\x1b[36m', 
 'red':'\x1b[91m', 
 'reset':'\x1b[0m'}

def set_start_time(start: datetime) -> None:
    """Define the time that the script started the execution.

    :param start: Datetime that the task execution started

    """
    global start_time
    start_time = start


def log(task_name: str, message: str) -> None:
    """Log message in standard color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message)


def ok(task_name: str, message: str) -> None:
    """Log message in green color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message, 'Ok')


def warn(task_name: str, message: str) -> None:
    """Log message in yellow color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message, 'Warning')


def fail(task_name: str, message: str) -> None:
    """Log message in red color.

    :param task_name: Name of the task to be printed
    :param message: The message itself

    """
    _print_message(task_name, message, 'Fail')


def _print_message(task_name: str, message: str, message_type: str='') -> None:
    """Print the received message formatted.

    :param task_name: str:
    :param message: str:
    :param message_type: str:  (Default value = '')

    """
    now_time = datetime.now() - start_time
    formatted_time = str(now_time).split('.')[0]
    output = '[{}{}{}]'.format(colors['cyan'], formatted_time, colors['reset'])
    output += '({}{}{}): '.format(colors['blue'], task_name, colors['reset'])
    if message_type == 'Ok':
        output += colors['green']
    else:
        if message_type == 'Warning':
            output += colors['yellow']
        else:
            if message_type == 'Fail':
                output += colors['red']
    output += message + colors['reset']
    print(output)


if __name__ == 'log':
    freeze_support()