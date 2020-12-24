# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intercept/utils.py
# Compiled at: 2018-12-27 16:24:21
# Size of source mod 2**32: 823 bytes
import re
from colorama import Fore
REGEXES = {'chat_event': re.compile('\\((?P<chat>\\s+?)\\) (?P<author>\\s+?): (?P<message>.+)')}
CONVERT = {'¬w':Fore.LIGHTWHITE_EX, 
 '¬W':Fore.LIGHTBLACK_EX, 
 '¬R':Fore.RED, 
 '¬r':Fore.LIGHTRED_EX, 
 '¬G':Fore.GREEN, 
 '¬g':Fore.LIGHTGREEN_EX, 
 '¬B':Fore.BLUE, 
 '¬b':Fore.LIGHTBLUE_EX, 
 '¬y':Fore.YELLOW, 
 '¬o':Fore.LIGHTYELLOW_EX, 
 '¬P':Fore.CYAN, 
 '¬p':Fore.LIGHTCYAN_EX, 
 '¬v':Fore.MAGENTA, 
 '¬V':Fore.LIGHTMAGENTA_EX, 
 '¬*':Fore.RESET, 
 '¬?':Fore.WHITE}

def without_color_codes(line: str) -> str:
    return re.sub('¬.', '', line)


def converted_color_codes(line: str) -> str:
    for k, v in CONVERT.items():
        line = line.replace(k, v)

    return line