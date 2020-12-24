# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/otfbot/lib/pluginSupport/decorators.py
# Compiled at: 2011-04-22 06:35:42


def callback(func):
    func.is_callback = True
    func.priority = 10
    return func


def callback_with_priority(priority):

    def decorator(func):
        func.is_callback = True
        func.priority = priority
        return func

    return decorator