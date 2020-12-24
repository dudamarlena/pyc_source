# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\carlo\projects\marlin\marlin\styles.py
# Compiled at: 2020-04-05 21:51:07
# Size of source mod 2**32: 719 bytes
from colorama import init
from colorama import Fore, Style
init(autoreset=True)

def label(label):
    labels = {'info':Fore.YELLOW + Style.BRIGHT + '[!]' + Style.RESET_ALL, 
     'bad':Fore.RED + Style.BRIGHT + '[-]' + Style.RESET_ALL, 
     'good':Fore.GREEN + Style.BRIGHT + '[+]' + Style.RESET_ALL, 
     'run':Fore.WHITE + Style.BRIGHT + '[~]' + Style.RESET_ALL, 
     'list':Fore.YELLOW + Style.BRIGHT + '>' + Style.RESET_ALL}
    return labels[label]


def color(color, text):
    colors = {'yellow':Fore.YELLOW + Style.BRIGHT + text + Style.RESET_ALL, 
     'red':Fore.RED + Style.BRIGHT + text + Style.RESET_ALL}
    return colors[color]