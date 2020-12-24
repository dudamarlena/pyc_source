# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/router.py
# Compiled at: 2020-03-04 16:40:12
# Size of source mod 2**32: 293 bytes


def action(methods=None, detail=False):
    if methods is None:
        methods = [
         'get']
    else:
        methods = [method.lower() for method in methods]

    def decorator(func):
        func.bind_to_methods = methods
        func.detail = detail
        return func

    return decorator