# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Mydemos_pkg\progress.py
# Compiled at: 2020-05-09 23:02:58
# Size of source mod 2**32: 300 bytes
from time import sleep

def progress_s(percent=0, width=30):
    left = width * percent // 100
    right = width - left
    print('\r[', ('#' * left), (' ' * right), ']', f" {percent:.0f}%", sep='', end='', flush=True)


def progress(s):
    for i in range(101):
        progress(i)
        sleep(s)