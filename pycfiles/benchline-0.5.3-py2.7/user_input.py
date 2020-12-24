# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/user_input.py
# Compiled at: 2014-03-25 00:18:33
"""
Functions for getting user input.
"""
import six, benchline.args

def validate_args(parser, options, args):
    pass


def select(prompt, valid_values):
    """
    Ask the user to select one of valid_values

    :param prompt: string presented to the user
    :param valid_values: list of strings
    :return: one of the string in valid_values
    """
    response = six.moves.input('%s [%s]: ' % (prompt, (', ').join(valid_values)))
    if response in valid_values:
        return response
    else:
        return select(prompt, valid_values)


def get_int(prompt):
    """Prompts the user for an int until they give one.
    :param prompt: string
    :return: the entered int
    """
    ans = six.moves.input(prompt)
    try:
        return int(ans)
    except ValueError:
        return get_int(prompt)


def main():
    benchline.args.go(__doc__, validate_args=validate_args)


if __name__ == '__main__':
    main()