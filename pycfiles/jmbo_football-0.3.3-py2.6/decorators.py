# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/football/decorators.py
# Compiled at: 2012-11-15 06:10:12
import sys
from django.conf import settings

class layered:
    """If a function or object with name "func_name + _ + layer" exists then it
    is called, else func is called normally."""

    def __init__(self, default='basic'):
        self.default = default

    def __call__(self, func):

        def new(request, *args, **kwargs):
            if hasattr(settings, 'FOUNDRY'):
                layers = settings.FOUNDRY['layers']
            else:
                layers = [
                 self.default]
            for layer in layers:
                method = getattr(sys.modules[func.__module__], '%s_%s' % (func.func_name, layer), None)
                if method is not None:
                    return method(request, *args, **kwargs)

            return func(request, *args, **kwargs)

        return new