# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/colors.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 1453 bytes
import os
if os.name != 'nt':
    if os.name != 'mac':

        class color:
            END = '\x1b[0m'
            BOLD = '\x1b[1m'
            RED = '\x1b[1;91m'
            GREEN = '\x1b[1;92m'
            ORANGE = '\x1b[1;93m'
            BLUE = '\x1b[1;94m'
            PURPLE = '\x1b[1;95m'
            UNDERLINE = '\x1b[4m'
            CYAN = '\x1b[1;96m'
            GREY = '\x1b[1;97m'
            BR = '\x1b[1;97;41m'
            BG = '\x1b[1;97;42m'
            BY = '\x1b[1;97;43m'


        O = '\x1b[1m \x1b[93m[!]\x1b[0m '
        R = '\x1b[1m \x1b[91m[-]\x1b[0m '
        GR = '\x1b[1m \x1b[97m[*]\x1b[0m '
        G = '\x1b[1m \x1b[92m[+]\x1b[0m '
        C = '\x1b[1m \x1b[96m[+]\x1b[0m '
else:

    class color:
        END = BOLD = RED = GREEN = ORANGE = BLUE = PURPLE = UNDERLINE = CYAN = GREY = BR = BG = BY = ''


    O = ' [!] '
    R = ' [-] '
    GR = ' [*] '
    G = ' [+] '
    C = ' [+] '