# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\toscawidgets\widgets\prototype\js.py
# Compiled at: 2007-04-03 20:32:27
from toscawidgets.api import JSLink, js_function
__all__ = ['prototype_js', 'S', 'Event']
prototype_js = JSLink(modname=__name__, filename='static/prototype.js')
S = js_function('$')

class Event:
    __module__ = __name__
    observe = js_function('Event.observe')