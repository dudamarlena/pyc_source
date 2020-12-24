# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/colors/colors.py
# Compiled at: 2020-03-10 16:51:28
# Size of source mod 2**32: 1240 bytes
from colorama import Fore
import re
color_regex = re.compile('(\x9b|\x1b\\[)[0-?]*[ -\\/]*[@-~]')

def strip_color(str):
    """Strip color from string."""
    return color_regex.sub('', str)


def len_color(str):
    """Compute how long the color escape sequences in the string are."""
    return len(str) - len(strip_color(str))


def ljust_with_color(str, n):
    """ljust string that might contain color."""
    return str.ljust(n + len_color(str))


class Colorizer(object):

    def __init__(self, use_color):
        self.use_color = use_color

    def set_use_color(self, use_color):
        self.use_color = use_color

    def get_use_color(self):
        return self.use_color

    def red(self, str):
        if self.use_color:
            return Fore.RED + str + Fore.RESET
        else:
            return str

    def green(self, str):
        if self.use_color:
            return Fore.GREEN + str + Fore.RESET
        else:
            return str

    def yellow(self, str):
        if self.use_color:
            return Fore.YELLOW + str + Fore.RESET
        else:
            return str

    def blue(self, str):
        if self.use_color:
            return Fore.BLUE + str + Fore.RESET
        else:
            return str