# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\all.py
# Compiled at: 2013-06-03 09:22:40
__doc__ = ' This is a module only to do a wild import of all pyojo modules.\n'
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