# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/tentapp/colors.py
# Compiled at: 2012-10-17 01:38:34
COLORS = {'red': '31', 'green': '32', 
   'yellow': '33', 
   'blue': '34', 
   'magenta': '35', 
   'cyan': '36', 
   'white': '37', 
   'reset': '39'}

def colorText(s, color):
    return '\x1b[%sm%s\x1b[%sm' % (COLORS[color], s, COLORS['reset'])


def red(s):
    return colorText(s, 'red')


def green(s):
    return colorText(s, 'green')


def yellow(s):
    return colorText(s, 'yellow')


def blue(s):
    return colorText(s, 'blue')


def magenta(s):
    return colorText(s, 'magenta')


def cyan(s):
    return colorText(s, 'cyan')


def white(s):
    return colorText(s, 'white')