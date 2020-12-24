# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pm/.local/lib/python3.5/site-packages/configurator/formats/_safe_importer.py
# Compiled at: 2016-05-20 05:07:39
# Size of source mod 2**32: 339 bytes
import sys, os
directory = os.path.dirname(os.path.abspath(__file__))
while sys.path.count(directory):
    sys.path.remove(directory)