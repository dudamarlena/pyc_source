# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/banner.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 3007 bytes
import time
from xsrfprobe import __version__
from xsrfprobe.core.colors import *

def banner():
    print('\n\n')
    time.sleep(0.05)
    print(color.ORANGE + '     _____       _____       _____      _____       _____                                    ')
    time.sleep(0.05)
    print(color.RED + '  __' + color.ORANGE + '|' + color.RED + '__ ' + color.ORANGE + '  |_  ' + color.RED + '__' + color.ORANGE + '|' + color.RED + '___ ' + color.ORANGE + ' |_  ' + color.RED + '__' + color.ORANGE + '|' + color.RED + '___  ' + color.ORANGE + '|_  ' + color.RED + '_' + color.ORANGE + '|' + color.RED + '____ ' + color.ORANGE + '|_' + color.RED + '   _' + color.ORANGE + '|' + color.RED + '____ ' + color.ORANGE + '|_ ' + color.RED + ' _____   _____  ______  ______  ')
    time.sleep(0.05)
    print(color.RED + ' \\  `  /    ' + color.ORANGE + '|' + color.RED + '|   ___|   ' + color.ORANGE + '|' + color.RED + '|  _  _|   ' + color.ORANGE + '|' + color.RED + '|   ___|  ' + color.ORANGE + '| ' + color.RED + '|   _  |  ' + color.ORANGE + '|' + color.RED + "|  _ ,' /     \\|  _   )|   ___| ")
    time.sleep(0.05)
    print(color.RED + '  >   <     ' + color.ORANGE + '|' + color.RED + ' `-.`-.    ' + color.ORANGE + '|' + color.RED + '|     \\    ' + color.ORANGE + '|' + color.RED + '|   ___|  ' + color.ORANGE + '|' + color.RED + ' |    __|  ' + color.ORANGE + '|' + color.RED + '|     \\ |  -  || |_  { |   ___| ')
    time.sleep(0.05)
    print(color.RED + ' /__/__\\   ' + color.ORANGE + '_|' + color.RED + '|______|  ' + color.ORANGE + '_|' + color.RED + '|__|\\__\\ ' + color.ORANGE + ' _|' + color.RED + '|___|   ' + color.ORANGE + ' _|' + color.RED + ' |___|   ' + color.ORANGE + ' _|' + color.RED + '|__|\\__\\\\_____/|______)|______| ')
    time.sleep(0.05)
    print(color.ORANGE + '    |_____|     |_____|     |_____|    |_____|     |_____| \n\n')
    time.sleep(0.05)


def banabout():
    print(color.BLUE + '   [---]            ' + color.GREY + 'XSRFProbe,' + color.RED + ' A' + color.ORANGE + ' Cross Site Request Forgery ' + color.RED + 'Audit Toolkit          ' + color.BLUE + '[---]')
    time.sleep(0.05)
    print(color.BLUE + '   [---]                                                                           [---]')
    time.sleep(0.05)
    print(color.BLUE + '   [---]   ' + color.PURPLE + '                    ' + color.GREEN + '~  Author : ' + color.CYAN + 'Pinaki Mondal  ~                   ' + color.BLUE + '     [---]')
    time.sleep(0.05)
    print(color.BLUE + '   [---]   ' + color.CYAN + '                   ~  github.com / ' + color.GREY + '0xInfection  ~                     ' + color.BLUE + '  [---]')
    time.sleep(0.05)
    print(color.BLUE + '   [---]                                                                           [---]')
    time.sleep(0.05)
    print(color.BLUE + '   [---]  ' + color.ORANGE + '                         ~  Version ' + color.RED + __version__ + color.ORANGE + '  ~                           ' + color.BLUE + '  [---]\n')
    time.sleep(0.05)