# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/justwatch/observer.py
# Compiled at: 2018-04-06 21:50:39
import time
from justwatch.objects import FileItem

class Observer(object):

    def __init__(self, manager):
        self.manager = manager
        self.callback = None
        return

    def set_callback(self, func):
        self.callback = func

    def watch(self):
        while True:
            for index, item in enumerate(self.manager.files_container):
                new_item = FileItem(item.path)
                if item != new_item:
                    self.callback(new_item)
                    self.manager.files_container[index] = new_item

            time.sleep(0.1)