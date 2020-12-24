# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\bulkrename\utils.py
# Compiled at: 2018-08-20 08:13:08
# Size of source mod 2**32: 1176 bytes
import sys

def exitcode(message):
    print(message)
    sys.exit(0)


def query_yes_no(question, default='yes'):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {'yes':True, 
     'y':True,  'ye':True,  'no':False,  'n':False}
    if default is None:
        prompt = ' [y/n] '
    elif default == 'yes':
        prompt = ' [Y/n] '
    elif default == 'no':
        prompt = ' [y/N] '
    else:
        raise ValueError(f"Invalid default answer: {default}")
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None:
            if choice == '':
                return valid[default]
        if choice in valid:
            return valid[choice]
        sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")