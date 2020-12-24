# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/pickup/file.py
# Compiled at: 2016-06-05 22:18:17


class File:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        f = open(self.file_path, 'r').readlines()
        return f