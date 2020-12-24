# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/xboomx/bin/xboomx_path.py
# Compiled at: 2014-04-17 06:27:45
import os
pathes = os.environ['PATH'].split(':')
for path in pathes:
    if os.path.isdir(path):
        for f in os.listdir(path):
            print f