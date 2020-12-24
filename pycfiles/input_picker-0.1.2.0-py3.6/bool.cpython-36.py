# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\input_picker\bool.py
# Compiled at: 2018-01-02 06:32:16
# Size of source mod 2**32: 1001 bytes
from .common import Option, ExceptionOption, Picker, Stop, Help

def pick_bool(*, defval: bool=True, use_bool_style: bool=False, raise_on_help: bool=True) -> bool:
    """ pick a bool value. """
    if not isinstance(defval, bool):
        raise TypeError('defval must be a bool value')
    else:
        options = Picker(sep='  ')
        if use_bool_style:
            options.add(Option('True', ['T', 'true'], True))
            options.add(Option('False', ['F', 'false'], False))
        else:
            options.add(Option('Yes', ['Y', 'yes'], True))
            options.add(Option('No', ['N', 'no'], False))
        options.add(ExceptionOption('Stop', ['S', 'stop'], Stop))
        if raise_on_help:
            options.add(ExceptionOption('Help', ['?', 'H'], Help))
        else:
            options.add(Option('Help', ['?', 'H'], Help))
    return options.pick(defval)