# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/parguments/cli.py
# Compiled at: 2013-05-25 02:13:25
import getpass
try:
    assert raw_input
except NameError:
    raw_input = input

def prompt(name, default=None):
    """
    Grab user input from command line.

    :param name: prompt text
    :param default: default value if no input provided.
    """
    prompt = name + (default and ' [%s]' % default or '')
    prompt += name.endswith('?') and ' ' or ': '
    while True:
        rv = raw_input(prompt)
        if rv:
            return rv
        if default is not None:
            return default

    return


def prompt_pass(name, default=None):
    """
    Grabs hidden (password) input from command line.

    :param name: prompt text
    :param default: default value if no input provided.
    """
    prompt = name + (default and ' [%s]' % default or '')
    prompt += name.endswith('?') and ' ' or ': '
    while True:
        rv = getpass.getpass(prompt)
        if rv:
            return rv
        if default is not None:
            return default

    return


def prompt_bool(name, default=False, yes_choices=None, no_choices=None):
    """
    Grabs user input from command line and converts to boolean
    value.

    :param name: prompt text
    :param default: default value if no input provided.
    :param yes_choices: default 'y', 'yes', '1', 'on', 'true', 't'
    :param no_choices: default 'n', 'no', '0', 'off', 'false', 'f'
    """
    yes_choices = yes_choices or ('y', 'yes', '1', 'on', 'true', 't')
    no_choices = no_choices or ('n', 'no', '0', 'off', 'false', 'f')
    while True:
        rv = prompt(name + '?', default and yes_choices[0] or no_choices[0])
        if rv.lower() in yes_choices:
            return True
        if rv.lower() in no_choices:
            return False


def prompt_choices(name, choices, default=None, no_choice=('none', )):
    """
    Grabs user input from command line from set of provided choices.

    :param name: prompt text
    :param choices: list or tuple of available choices.
    :param default: default value if no input provided.
    :param no_choice: acceptable list of strings for "null choice"
    """
    _choices = []
    options = []
    for choice in choices:
        options.append(choice)
        _choices.append(choice)

    while True:
        rv = prompt(name + '? - (%s)' % (', ').join(options), default)
        rv = rv.lower()
        if rv in no_choice:
            return
        if rv in _choices:
            return rv

    return