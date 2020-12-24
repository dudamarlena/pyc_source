# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shliyana/anaconda3/lib/python3.7/site-packages/htrc/lib/cli.py
# Compiled at: 2019-05-06 10:39:58
# Size of source mod 2**32: 1162 bytes
from builtins import input

def bool_prompt(prompt_str, default=None):
    if default is True:
        default = 'y'
    else:
        if default is False:
            default = 'n'
    result = prompt(prompt_str, options=['y', 'n'], default=default)
    if result == 'y':
        return True
    if result == 'n':
        return False


def prompt(prompt, options=None, default=None):
    prompt = '\n' + prompt
    if options:
        choices = options[:]
        if default:
            if default in choices:
                default_idx = choices.index(default)
                choices[default_idx] = choices[default_idx].upper()
        prompt += ' [{0}]'.format('/'.join(choices))
    else:
        if default:
            if isinstance(default, str):
                prompt += ' [Default: {0}]'.format(default.encode('utf-8'))
            else:
                prompt += ' [Default: {0}]'.format(default)
    prompt += ' '
    result = None
    while not result is None:
        if not options or result not in options:
            result = input(prompt)
            result = result.lower().strip()
            if default and result == '':
                result = default

    return result