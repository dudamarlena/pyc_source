# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/ext/annotation.py
# Compiled at: 2016-04-25 13:24:08
# Size of source mod 2**32: 2867 bytes
"""Python 3 function annotation typecasting support."""
from __future__ import unicode_literals
from inspect import ismethod, getfullargspec
from web.core.compat import items

class AnnotationExtension(object):
    __doc__ = 'Utilize Python 3 function annotations as a method to filter arguments coming in from the web.\n\t\n\tArgument annotations are treated as callbacks to execute, passing in the unicode value coming in from the web and\n\tswapping it with the value returned by the callback. This allows for trivial typecasting to most built-in Python\n\ttypes such as `int`, `float`, etc., as well as creative use such as `\',\'.split` to automatically split a comma-\n\tseparated value. One can of course also write custom callbacks, notably ones that raise `HTTPException`\n\tsubclasses to not appear as an Internal Server Error.\n\t\n\tFor example:\n\t\n\t\tdef multiply(a: int, b: int):\n\t\t\treturn str(a * b)\n\t\n\tThis extension also performs a utility wrapping of returned values in the form of a 2-tuple of the return\n\tannotation itself and the value returned by the callable endpoint. This integrates well with the view registered\n\tby the `web.template` package to define a template at the head of the function, returning data for the template\n\tto consume:\n\t\n\t\tdef hello(name="world"): -> \'mako:hello.html\'\n\t\t\treturn dict(name=name)\n\t\n\tIf your editor has difficulty syntax highlighting such annotations, check for a Python 3 compatible update to your\n\teditor\'s syntax definitions.\n\t'
    __slots__ = tuple()
    provides = [
     'annotation', 'cast', 'typecast']

    def mutate(self, context, handler, args, kw):
        """Inspect and potentially mutate the given handler's arguments.
                
                The args list and kw dictionary may be freely modified, though invalid arguments to the handler will fail.
                """
        annotations = getattr(handler.__func__ if hasattr(handler, '__func__') else handler, '__annotations__', None)
        if not annotations:
            return
        argspec = getfullargspec(handler)
        arglist = list(argspec.args)
        if ismethod(handler):
            del arglist[0]
        for i, value in enumerate(list(args)):
            key = arglist[i]
            if key in annotations:
                args[i] = annotations[key](value)

        for key, value in list(items(kw)):
            if key in annotations:
                kw[key] = annotations[key](value)

    def transform(self, context, handler, result):
        """Transform the value returned by the controller endpoint.
                
                This extension transforms returned values if the endpoint has a return type annotation.
                """
        handler = handler.__func__ if hasattr(handler, '__func__') else handler
        annotation = getattr(handler, '__annotations__', {}).get('return', None)
        if annotation:
            return (annotation, result)
        return result