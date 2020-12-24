# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/.virtualenvs/temp3/lib/python3.4/site-packages/colordiffs/cmdline.py
# Compiled at: 2015-06-21 18:32:50
# Size of source mod 2**32: 71 bytes
import sys
from .colordiffs import run

def main():
    run(sys.stdin)