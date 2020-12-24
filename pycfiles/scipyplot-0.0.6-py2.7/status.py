# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipyplot/log/status.py
# Compiled at: 2016-12-01 23:07:35
from __future__ import print_function
from colorama import Fore
import scipyplot.utils as rutils, sys

def cnd_status(current_verbosity, necessary_verbosity, f, cnt_verbosity=float('inf'), indent=0):
    if necessary_verbosity < current_verbosity:
        rutils.indent(indent)
        status(f)


def status(f):
    """

    :param f:
    :return:
    """
    if f == 0:
        print('[' + Fore.GREEN + 'Done' + Fore.RESET + ']')
    if f < 0:
        print('[' + Fore.RED + 'Error' + Fore.RESET + ']')
    if f > 0:
        print('[' + Fore.MAGENTA + '???' + Fore.RESET + ']')
    sys.stdout.flush()