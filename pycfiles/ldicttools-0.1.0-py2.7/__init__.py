# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ldicttools/__init__.py
# Compiled at: 2017-08-19 00:04:54
import threading
from .implementation import Dictionary

class DictionaryThread(threading.Thread):

    def __init__(self, dictionary):
        threading.Thread.__init__(self)
        self.dict = dictionary
        self.daemon = True
        self.dictionaryobject = None
        return

    def run(self):
        self.dictionaryobject = Dictionary(self.dict)

    def isFinished(self):
        return self.dictionaryobject is not None

    def getObject(self):
        return self.dictionaryobject


def getDict(file):
    thread = DictionaryThread(file)
    thread.start()
    return thread