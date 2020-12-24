# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/tw/extjs/extensions.py
# Compiled at: 2008-09-03 16:29:00
from base import ExtJSLinkAutoInit, all_debug, all
from tw.api import JSLink
autogrid_debug_js = ExtJSLinkAutoInit(modname=__name__, filename='static/ux/autogrid.js', javascript=[
 all_debug])
autogrid_js = ExtJSLinkAutoInit(modname=__name__, filename='static/ux/autogrid.js', javascript=[
 all])
spotlight_js = JSLink(modname=__name__, filename='static/ux/Spotlight.js')