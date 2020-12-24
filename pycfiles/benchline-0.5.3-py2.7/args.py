# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/benchline/args.py
# Compiled at: 2014-05-13 17:55:07
"""
Command-line argument processing functions
"""
from optparse import OptionParser

def make_parser(doc='', usage=None, add_options=True):
    """Make a parser object.

    :param doc:
    :param usage:
    :param add_options: default True whether to add -v and -t options by default
    :return: None
    """
    if not usage:
        usage = 'usage: %%prog [options]\n%s' % doc
    parser = OptionParser()
    if usage:
        parser.set_usage(usage)
    if add_options:
        parser.add_option('-v', '--verbose', action='store_true', help='run gregariously')
        parser.add_option('-t', '--doctest', action='store_true', help='run doctests and exit')
    return parser


def triage(parser, main=None, validate_args=None):
    """Triage the command-line presented.

    :param parser:
    :param main:
    :param validate_args:
    :return:
    """
    options, args = parser.parse_args()
    if options.doctest or not main:
        import doctest
    if validate_args:
        validate_args(parser, options, args)
        doctest.testmod(verbose=options.verbose)
    elif main:
        main()
    return (
     options, args)


def go(doc='', usage=None, validate_args=None):
    """Wrapper function to do everything

    :param doc:
    :param usage:
    :param validate_args:
    :return: options, args
    """
    parser = make_parser(doc, usage)
    return triage(parser, validate_args=validate_args)


def get_arg(args, num):
    """Returns the num value from args
    without throwing an annoying exception
    when num is too large.

    >>> get_arg([0], 0)
    0
    >>> get_arg([0], 1)
    ''
    >>> get_arg([0, 1, 2, 3], 5)
    ''
    >>> get_arg([0, 1, 2, 3], 2)
    2

    :param num:
    :return: string arg value
    """
    if len(args) >= num + 1:
        return args[num]
    else:
        return ''


if __name__ == '__main__':
    go(__doc__)