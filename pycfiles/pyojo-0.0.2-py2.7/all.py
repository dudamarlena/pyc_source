# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyojo\all.py
# Compiled at: 2013-06-03 09:22:40
""" This is a module only to do a wild import of all pyojo modules.
"""
import os, sys, pyojo
from pyojo.func import pretty
import pyojo.js as js
from pyojo.js import dojo
from pyojo.js import dijit
from pyojo.js.dojo import store
from pyojo.js.dijit import layout
from pyojo.js.dijit import form
from pyojo.js.dijit.icons import ICON, ICON_EDIT
__all__ = [
 'os',
 'sys',
 'pyojo',
 'pretty',
 'js',
 'dojo',
 'dijit',
 'store',
 'layout',
 'form',
 'ICON',
 'ICON_EDIT']