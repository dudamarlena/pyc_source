# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/makesense/prompt.py
# Compiled at: 2014-10-21 08:35:55
"""
makesense.prompt
---------------------

Functions for prompting the user for project info.
"""
from __future__ import unicode_literals
import sys
PY3 = sys.version > b'3'
if PY3:
    iteritems = lambda d: iter(d.items())
else:
    input = raw_input
    iteritems = lambda d: d.iteritems()

def prompt_for_config(context):
    """
    Prompts the user to enter new config, using context as a source for the
    field names and sample values.
    """
    makesense_dict = {}
    for key, val in iteritems(context[b'makesense']):
        prompt = (b'{0} (default is "{1}")? ').format(key, val)
        if PY3:
            new_val = input(prompt.encode(b'utf-8'))
        else:
            new_val = input(prompt.encode(b'utf-8')).decode(b'utf-8')
        new_val = new_val.strip()
        if new_val == b'':
            new_val = val
        makesense_dict[key] = new_val

    return makesense_dict


def query_yes_no(question, default=b'yes'):
    """
    Ask a yes/no question via `raw_input()` and return their answer.

    :param question: A string that is presented to the user.
    :param default: The presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Adapted from
    http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    http://code.activestate.com/recipes/577058/

    """
    valid = {b'yes': True, b'y': True, b'ye': True, b'no': False, b'n': False}
    if default is None:
        prompt = b' [y/n] '
    else:
        if default == b'yes':
            prompt = b' [Y/n] '
        elif default == b'no':
            prompt = b' [y/N] '
        else:
            raise ValueError(b"invalid default answer: '%s'" % default)
        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == b'':
                return valid[default]
            if choice in valid:
                return valid[choice]
            sys.stdout.write(b"Please respond with 'yes' or 'no' (or 'y' or 'n').\n")

    return