# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sara_bs\sara_bs.py
# Compiled at: 2020-04-28 15:27:38
# Size of source mod 2**32: 538 bytes
"""
Created on Tue Apr 28 21:32:59 2020

@author: Sara Ben Shabbat
"""
author_name = 'Sara Ben Shabbat'

def hello_world() -> None:
    print('Hello World !')


class fruit:

    def __init__(self, name, color):
        self.name = name
        self.color = color

    def print_fruit_attributes(self):
        print('The fruit name is = ' + self.name)
        print('The fruit color is = ' + self.color)