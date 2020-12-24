# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cantools/hooks.py
# Compiled at: 2017-11-19 19:41:56


class HookBox(object):

    def __init__(self):
        self.hooks = []

    def __call__(self, data):
        for hook in self.hooks:
            hook(data)

    def register(self, cb):
        self.hooks.append(cb)


memhook = HookBox()
dbhook = HookBox()