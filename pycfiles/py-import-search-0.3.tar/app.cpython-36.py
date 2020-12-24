# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/lucas.selfslagh/anaconda3/lib/python3.6/site-packages/pyimdf/app.py
# Compiled at: 2019-06-30 10:41:25
# Size of source mod 2**32: 151 bytes
from imdf.venue import Venue
import os

def run():
    print('app run')
    print(os.getcwd())
    v = Venue()


if __name__ == '__main__':
    run()