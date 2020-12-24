# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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