# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/ui/base.py
# Compiled at: 2019-08-15 14:28:42
# Size of source mod 2**32: 948 bytes
from typing import Dict
from functools import wraps
from prompt_toolkit import HTML, print_formatted_text
from hermit.errors import HermitError
from hermit.qrcode import displayer, reader
DeadTime = 30

def clear_screen():
    print(chr(27) + '[2J')


def reset_screen():
    print(chr(27) + 'c')


def command(name, commands: Dict):

    def _command_decorator(f):
        nonlocal name
        if name is None:
            name = f.name
        if name in commands:
            raise Exception('command already defined: ' + name)

        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except TypeError as terr:
                try:
                    raise terr
                finally:
                    terr = None
                    del terr

            except Exception as err:
                try:
                    print(err)
                    raise HermitError('Hmm. Something went wrong.')
                finally:
                    err = None
                    del err

        commands[name] = wrapper
        return wrapper

    return _command_decorator