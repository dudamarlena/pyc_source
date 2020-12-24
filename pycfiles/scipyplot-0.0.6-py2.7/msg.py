# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/log/msg.py
# Compiled at: 2016-12-01 23:07:35
from __future__ import print_function
from scipyplot.utils import indent
from colorama import Fore
import logging
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


def msg(string, indent_depth=0, eol=True):
    assert indent_depth >= 0
    log_msg(string)
    indent(indent_depth)
    if eol:
        print(string)
    else:
        print(string, end='')


def log_msg(string):
    logging.getLogger(__name__).addHandler(NullHandler())
    logging.info(string)


def cnd_msg(current_verbosity, necessary_verbosity, string, indent_depth=0, cnt_verbosity=float('inf'), eol=False):
    """

    :param current_verbosity:
    :param necessary_verbosity:
    :param string: String to be logged
    :param indent_depth: Indentation level
    :param cnt_verbosity:
    :param eol:
    :return:
    """
    if necessary_verbosity < current_verbosity:
        msg(string, indent_depth, eol=False)
        if cnt_verbosity is not float('inf'):
            if eol:
                print('\n', end='')
            elif current_verbosity < cnt_verbosity:
                print('... ', end='')
            else:
                print(':\n', end='')
    else:
        log_msg(string)
    return [
     current_verbosity, necessary_verbosity, indent_depth, cnt_verbosity]


def cnd_warning(current_verbosity, necessary_verbosity, string, indent_depth=0, cnt_verbosity=float('inf'), eol=False):
    if necessary_verbosity < current_verbosity:
        msg(string, indent_depth, eol=False)
    else:
        log_warning(string)


def warning(string):
    log_warning(string)
    msg(color('Warning: ' + string, 'red'))


def log_warning(string):
    logging.getLogger(__name__).addHandler(NullHandler())
    logging.warning(string)


def color(string, color):
    out = Fore.RED + string + Fore.RESET
    return out