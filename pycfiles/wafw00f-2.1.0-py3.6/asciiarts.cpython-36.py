# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wafw00f/lib/asciiarts.py
# Compiled at: 2020-02-20 22:34:09
# Size of source mod 2**32: 2476 bytes
"""
Copyright (C) 2020, WAFW00F Developers.
See the LICENSE file for copying permission.
"""
from sys import platform
from random import randint
from wafw00f import __version__
W = '\x1b[1;97m'
Y = '\x1b[1;93m'
G = '\x1b[1;92m'
R = '\x1b[1;91m'
B = '\x1b[1;94m'
C = '\x1b[1;96m'
E = '\x1b[0m'
if 'win' in platform:
    W = Y = G = R = B = C = E = ''

def randomArt():
    woof = '\n                   ' + W + '______\n                  ' + W + '/      \\\n                 ' + W + '(  Woof! )\n                  ' + W + '\\  ____/                      ' + R + ')\n                  ' + W + ',,                           ' + R + ') (' + Y + '_\n             ' + Y + '.-. ' + W + '-    ' + G + '_______                 ' + R + '( ' + Y + '|__|\n            ' + Y + '()``; ' + G + '|==|_______)                ' + R + '.)' + Y + '|__|\n            ' + Y + "/ ('        " + G + '/|\\                  ' + R + '(  ' + Y + '|__|\n        ' + Y + '(  /  )       ' + G + ' / | \\                  ' + R + '. ' + Y + '|__|\n         ' + Y + '\\(_)_))      ' + G + '/  |  \\                   ' + Y + '|__|' + E + '\n\n                    ' + C + '~ WAFW00F : ' + B + 'v' + __version__ + ' ~' + W + '\n    The Web Application Firewall Fingerprinting Toolkit\n    ' + E
    w00f = '\n                ' + W + '______\n               ' + W + '/      \\\n              ' + W + '(  W00f! )\n               ' + W + '\\  ____/\n               ' + W + ',,    ' + G + '__            ' + Y + '404 Hack Not Found\n           ' + C + '|`-.__   ' + G + '/ /                     ' + R + ' __     __\n           ' + C + '/"  _/  ' + G + '/_/                       ' + R + '\\ \\   / /\n          ' + B + '*===*    ' + G + '/                          ' + R + '\\ \\_/ /  ' + Y + '405 Not Allowed\n         ' + C + '/     )__//                           ' + R + '\\   /\n    ' + C + '/|  /     /---`                        ' + Y + '403 Forbidden\n    ' + C + '\\\\/`   \\ |                                 ' + R + '/ _ \\\n    ' + C + '`\\    /_\\\\_              ' + Y + '502 Bad Gateway  ' + R + '/ / \\ \\  ' + Y + '500 Internal Error\n      ' + C + '`_____``-`                             ' + R + '/_/   \\_\\\n\n                        ' + C + '~ WAFW00F : ' + B + 'v' + __version__ + ' ~' + W + '\n        The Web Application Firewall Fingerprinting Toolkit\n    ' + E
    arts = [
     woof, w00f]
    return arts[randint(0, 1)]