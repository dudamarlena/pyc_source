# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\input_picker\colors.py
# Compiled at: 2018-01-04 06:53:31
# Size of source mod 2**32: 816 bytes
import colorama

def lightred(text):
    return colorama.Fore.LIGHTRED_EX + text + colorama.Fore.RESET


def lightgreen(text):
    return colorama.Fore.LIGHTGREEN_EX + text + colorama.Fore.RESET