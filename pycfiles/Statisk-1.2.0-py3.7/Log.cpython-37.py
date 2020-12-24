# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/statisk/Log.py
# Compiled at: 2020-01-15 09:20:16
# Size of source mod 2**32: 1314 bytes
from termcolor import colored, cprint
ascii_title = ' ▄▄▄· ▄· ▄▌.▄▄ · ▄▄▄▄▄ ▄▄▄· ▄▄▄▄▄▪  .▄▄ · ▄ •▄ \n▐█ ▄█▐█▪██▌▐█ ▀. •██  ▐█ ▀█ •██  ██ ▐█ ▀. █▌▄▌▪\n ██▀·▐█▌▐█▪▄▀▀▀█▄ ▐█.▪▄█▀▀█  ▐█.▪▐█·▄▀▀▀█▄▐▀▀▄·\n▐█▪·• ▐█▀·.▐█▄▪▐█ ▐█▌·▐█ ▪▐▌ ▐█▌·▐█▌▐█▄▪▐█▐█.█▌\n.▀     ▀ •  ▀▀▀▀  ▀▀▀  ▀  ▀  ▀▀▀ ▀▀▀ ▀▀▀▀ ·▀  ▀'

def title():
    line_break()
    green(ascii_title)
    line_break()


def error(message):
    cprint('Error: %s' % message, 'red')


def fatal_error(message):
    line_break()
    cprint('Fatal Error: %s' % message, 'red')
    line_break()
    exit(-1)


def red(message):
    print(colored(message, 'red'))


def salmon(message):
    print('\x1b[91m' + message + '\x1b[0m')


def purple(message):
    print('\x1b[95m' + message + '\x1b[0m')


def blue(message):
    print('\x1b[94m' + message + '\x1b[0m')


def green(message):
    cprint(message, 'green')


def grey(message):
    cprint(message, 'grey')


def line_break():
    print('')