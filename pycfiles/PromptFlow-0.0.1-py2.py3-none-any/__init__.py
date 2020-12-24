# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/dave/checkouts/prompter/build/lib/prompter/__init__.py
# Compiled at: 2015-01-13 23:55:22
__doc__ = "\nprompter CUI input prompts\n~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nPrompter is a tool for displaying simple input prompts with optional defaults.\n\nUsage:\n\n    >>> from prompter import prompt, yesno\n\n    >>> prompt('What is your name?')\n    What is your name? Dave\n    'Dave'\n\n    >>> prompt('What is your name?', default='Jenn')\n    What is your name? [Jenn]\n    'Jenn'\n\n    >>> prompt('What is your name?', default='Jenn', suffix='\n > ')\n    What is your name? [Jenn]\n     >\n    'Jenn'\n\n    >>> prompt('Enter text surrounded by spaces.', strip=False)\n    Enter text surrounded by spaces.    text\n    '   text   '\n\n    >>> yesno('Really?')\n    Really? [Y/n]\n    True\n\n    >>> yesno('Really?')\n    Really? [Y/n] no\n    False\n\n    >>> yesno('Really?', default='no')\n    Really? [y/N]\n    True\n\n    >>> yesno('')\n    [Y/n] n\n    False\n\n:copyright: (c) 2014 by Dave Forgac\n:license: MIT, see LICENSE file for details\n"
from __future__ import print_function
import re
__title__ = 'prompter'
__author__ = 'Dave Forgac'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014 Dave Forgac'
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

def get_input(message=None):
    """ Get user input using raw_input() for Python 2.x and input() for 3.x. """
    try:
        return raw_input(message)
    except NameError:
        return input(message)


def prompt(message, default=None, strip=True, suffix=' '):
    """ Print a message and prompt user for input. Return user input. """
    if default is not None:
        prompt_text = ('{0} [{1}]{2}').format(message, default, suffix)
    else:
        prompt_text = ('{0}{1}').format(message, suffix)
    input_value = get_input(prompt_text)
    if input_value and strip:
        input_value = input_value.strip()
    if not input_value:
        input_value = default
    return input_value


def yesno(message, default='yes', suffix=' '):
    """ Prompt user to answer yes or no. Return True if the default is chosen,
     otherwise False. """
    if default == 'yes':
        yesno_prompt = '[Y/n]'
    else:
        if default == 'no':
            yesno_prompt = '[y/N]'
        else:
            raise ValueError("default must be 'yes' or 'no'.")
        if message != '':
            prompt_text = ('{0} {1}{2}').format(message, yesno_prompt, suffix)
        else:
            prompt_text = ('{0}{1}').format(yesno_prompt, suffix)
        while True:
            response = get_input(prompt_text).strip()
            if response == '':
                return True
            if re.match('^(y)(es)?$', response, re.IGNORECASE):
                if default == 'yes':
                    return True
                else:
                    return False

            elif re.match('^(n)(o)?$', response, re.IGNORECASE):
                if default == 'no':
                    return True
                else:
                    return False