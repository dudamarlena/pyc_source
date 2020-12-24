# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: test.py
# Compiled at: 2017-04-23 17:05:07
import atproject.Download.main as dl

def get(str):
    path = str
    obj = dl.CustomLibrary()
    obj.torrent_path = path
    path_to_file = obj.get()