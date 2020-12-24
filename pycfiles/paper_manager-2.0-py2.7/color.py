# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cer/Project/pycharm/paper_manager/paper_manager/color.py
# Compiled at: 2018-04-14 05:20:12
from colorama import init, Fore, Back, Style
init(autoreset=True)
colors = ['red', 'green', 'yellow',
 'blue', 'magenta', 'cyan',
 'white']

class Colored(object):

    def red(self, s):
        return Fore.RED + s + Fore.RESET

    def green(self, s):
        return Fore.GREEN + s + Fore.RESET

    def yellow(self, s):
        return Fore.YELLOW + s + Fore.RESET

    def blue(self, s):
        return Fore.BLUE + s + Fore.RESET

    def magenta(self, s):
        return Fore.MAGENTA + s + Fore.RESET

    def cyan(self, s):
        return Fore.CYAN + s + Fore.RESET

    def white(self, s):
        return Fore.WHITE + s + Fore.RESET

    def black(self, s):
        return Fore.BLACK

    def white_green(self, s):
        return Fore.WHITE + Back.GREEN + s + Fore.RESET + Back.RESET

    def yellow_blue(self, s):
        return Fore.YELLOW + Back.BLUE + s + Fore.RESET + Back.RESET

    def blue_yellow(self, s):
        return Fore.BLUE + Back.YELLOW + s + Fore.RESET + Back.RESET

    def paint(self, color, string):
        return eval(("self.{}('{}')").format(color, string))