# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mastermind/params.py
# Compiled at: 2020-02-20 02:54:44
# Size of source mod 2**32: 960 bytes
""" params for mastermind """
from colorama import Fore, Style
count_turns = 10
guess_peg = '⬤'
count_colors = 6
color_dict = {'r':Fore.RED + Style.BRIGHT, 
 'g':Fore.GREEN + Style.BRIGHT, 
 'y':Fore.YELLOW, 
 'b':Fore.BLUE, 
 'm':Fore.MAGENTA, 
 'w':Fore.WHITE}
count_boxes = 4
answer_dict = {'1':'◍', 
 '2':'○',  '9':'_'}
debug = False