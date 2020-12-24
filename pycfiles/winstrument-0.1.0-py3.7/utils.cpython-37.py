# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\utils.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 3470 bytes
from winstrument.data.module_message import ModuleMessage
from tabulate import tabulate
import json
from collections import namedtuple
import os

def format_table(messagelist, verbosity=0):
    if verbosity < 1:
        return tabulate([elipsize_message(message).flatten() for message in messagelist], headers='keys')
    return tabulate([message.flatten() for message in messagelist], headers='keys')


def format_json(messagelist, verbosity=0):
    return json.dumps([message.flatten() for message in messagelist])


def mask_to_str(mask, enum_map):
    """
    Attempts to produce a string of set flags from the given mask and dict of enum value-to-name mappings
    mask: int - bitmask from e.g. Windows API
    enum_map: dict[int -> str]
    returns a string in the form: FLAG 1 | FLAG 2 ...
    """
    flags_set = []
    for flag in enum_map.keys():
        if mask & flag == flag:
            flags_set.append(enum_map[flag])

    return ' | '.join(flags_set)


def format_grep(messagelist, verbosity=0):
    outlines = []
    sep = '|'
    for message in messagelist:
        outline = f"{message.module}{sep}{message.time}{sep}{message.target}"
        for k, v in message.data.items():
            outline += f"{sep}{k}:{v}"

        outlines.append(outline)

    return '\n'.join(outlines)


def elipsize_path(path):
    """
    Converts a full Windows path into a path like C:/.../filename.exe
    path - str
    Return - shortened path: str
    """
    path_start, tail = os.path.splitdrive(path)
    last_part = os.path.split(tail)[(-1)]
    return f"{path_start}/.../{last_part}"


def elipsize_message(message):
    """
    Creates a new message from the original with the target path shortend
    """
    new_target = elipsize_path(message.target)
    return ModuleMessage((message.module), new_target, (message.data), time=(message.time))


def get_formatters():
    """
    Returns namedtuple of all available formatters and human readable names
    Fields:
    name - human readable name for use in command arguments etc
    function - function object to the formatter
    """
    Formatter = namedtuple('Formatter', 'name function')
    formatters = [Formatter(name='table', function=format_table),
     Formatter(name='json', function=format_json),
     Formatter(name='grep', function=format_grep)]
    return formatters


def get_formatter(name):
    """
    Returns the formatter callback for the formatter with the speicfied name.
    Returns None if no such formatter exists
    """
    formatter_list = get_formatters()
    for formatter in formatter_list:
        if name.lower() == formatter.name.lower():
            return formatter.function

    raise ValueError(f"No formatter {name}")