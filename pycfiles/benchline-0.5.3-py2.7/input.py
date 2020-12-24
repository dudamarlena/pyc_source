# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/input.py
# Compiled at: 2014-03-23 22:25:48
"""
Functions for getting user input.
"""
import benchline.args
try:
    input = raw_input
except NameError:
    pass

def validate_args(parser, options, args):
    pass


def select(prompt, valid_values):
    """
    Ask the user to select one of valid_values

    :param prompt: string presented to the user
    :param valid_values: list of strings
    :return: one of the string in valid_values
    """
    response = input(prompt)
    if response in valid_values:
        return response
    else:
        return select(prompt, valid_values)


def main():
    benchline.args.go(__doc__, validate_args=validate_args)


if __name__ == '__main__':
    main()