# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/BoundMethod.py
# Compiled at: 2008-09-03 09:02:13
from pyjamas.__pyjamas__ import JS

def BoundMethod(obj, method):
    """
        Return a javascript-compatible callable which can be used as a "bound method".
        
        Javascript doesn't support callables, and it doesn't support bound methods,
        so you can't use those in pyjamas currently.
        
        This is an OK workaround.
    """
    JS('\n        return function() {\n            return method.apply(obj, arguments);\n        };\n    ')