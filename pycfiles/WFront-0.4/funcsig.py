# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jek/projects/oss/src/wfront-work/docs/source/_lib/funcsig.py
# Compiled at: 2008-12-27 22:57:02
import inspect

def callable_fixer(app, what, name, obj, options, signature, return_annotation):
    if what == 'attribute':
        print name
    if what == 'function' and signature is None and hasattr(obj, '__call__'):
        spec = inspect.getargspec(obj.__call__)
        spec[0].pop(0)
        signature = inspect.formatargspec(*spec)
    return (
     signature, return_annotation)


def setup(app):
    app.connect('autodoc-process-signature', callable_fixer)