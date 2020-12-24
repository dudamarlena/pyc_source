# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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