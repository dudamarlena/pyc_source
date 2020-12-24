# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/prototype/js.py
# Compiled at: 2008-06-02 11:15:04
from tw.api import JSLink, js_function
__all__ = ['prototype_js', 'S', 'Event']
prototype_js = JSLink(modname=__name__, filename='static/prototype.js')
S = js_function('$')

class Event:
    observe = js_function('Event.observe')