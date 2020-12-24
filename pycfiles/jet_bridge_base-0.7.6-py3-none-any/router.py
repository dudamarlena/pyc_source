# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/router.py
# Compiled at: 2019-10-06 12:57:02


def action(methods=list(['get']), detail=False):
    methods = [ method.lower() for method in methods ]

    def decorator(func):
        func.bind_to_methods = methods
        func.detail = detail
        return func

    return decorator