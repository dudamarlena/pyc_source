# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/snoopdroid/snoopdroid/ui.py
# Compiled at: 2020-04-03 08:08:14
# Size of source mod 2**32: 2145 bytes
from tqdm import tqdm
from colorama import init
from termcolor import colored
from .constants import __version__

def logo():
    print('                                   _           _     _      ')
    print('                                  | |         (_)   | |     ')
    print('   ___ _ __   ___   ___  _ __   __| |_ __ ___  _  __| |     ')
    print("  / __| '_ \\ / _ \\ / _ \\| '_ \\ / _` | '__/ _ \\| |/ _` |")
    print('  \\__ \\ | | | (_) | (_) | |_) | (_| | | | (_) | | (_| |   ')
    print('  |___/_| |_|\\___/ \\___/| .__/ \\__,_|_|  \\___/|_|\\__,_|')
    print('                        | |                                 ')
    print('                        |_|                    v{}          '.format(__version__))
    print('                                                            ')


class PullProgress(tqdm):

    def update_to(self, file_name, current, total):
        if total is not None:
            self.total = total
        self.update(current - self.n)


init(autoreset=True)

def info(text):
    return colored('***', 'cyan', attrs=['bold']) + ' ' + text


def error(text):
    return colored('!!!', 'red', attrs=['bold']) + ' Error: ' + text


def highlight(text):
    return colored(text, 'cyan', attrs=['bold'])


def green(text):
    return colored(text, 'green', attrs=['bold'])


def red(text):
    return colored(text, 'red', attrs=['bold'])