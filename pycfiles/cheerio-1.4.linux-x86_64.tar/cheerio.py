# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucy/lib/python2.7/site-packages/cheerio/cheerio.py
# Compiled at: 2014-08-26 02:27:52
from goodbye import *
import random

def cheerio():
    a = random.randint(0, len(goodbyes) - 1)
    color = random.randint(0, len(colors) - 1)
    print colors[color] + goodbyes[a] + '\x1b[0m'


if __name__ == '__main__':
    cheerio()