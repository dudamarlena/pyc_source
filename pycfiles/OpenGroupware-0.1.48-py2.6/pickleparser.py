# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/picklejar/pickleparser.py
# Compiled at: 2012-10-12 07:02:39
import pickle

class PickleParser:

    def __init__(self):
        pass

    def dict_from_string(self, data):
        return self.propertyListFromString(data)

    def propertyListFromString(self, data):
        return pickle.loads(data)