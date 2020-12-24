# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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