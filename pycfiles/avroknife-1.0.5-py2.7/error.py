# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/removing_madis_from_code/avroknife/avroknife/error.py
# Compiled at: 2015-09-04 08:27:04
from __future__ import print_function
import sys

def error(message):
    print(('ERROR: {}').format(message), file=sys.stderr)