# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/StoreData/__init__.py
# Compiled at: 2015-09-14 00:09:41
"""
    create a test class to test pickle
"""

class StoreData:

    def __init__(self):
        self.data = [
         1, 2, 3]

    def set_data(self, data):
        self.data = data