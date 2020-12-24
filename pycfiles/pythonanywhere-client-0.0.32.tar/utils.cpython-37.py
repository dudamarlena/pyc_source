# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ABRA\Desktop\programlarim\hakancelik96\pythonanywhere-python-client\pythonanywhere_client\utils.py
# Compiled at: 2019-07-02 11:20:30
# Size of source mod 2**32: 330 bytes


def client_decorator(op, name='', path='', data=dict()):

    def client_f(func):

        def wraps(*args, **kwargs):
            client = args[0].client
            function_name = func.__name__
            return getattr(client, '_requests')(function_name, op, name, path, data)

        return wraps

    return client_f