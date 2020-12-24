# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: server.py
# Compiled at: 2014-08-18 16:55:08
import os
from oneline import ol
if __name__ == '__main__':
    print os.getcwd()
    server = ol.server()
    server.start()