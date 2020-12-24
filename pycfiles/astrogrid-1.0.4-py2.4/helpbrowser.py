# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-9.6.0-i386/egg/astrogrid/helpbrowser.py
# Compiled at: 2007-05-29 11:51:01
__id__ = '$Id: helpbrowser.py 97 2007-05-29 15:51:00Z eddie $'
import os, sys

def open(filename):
    if sys.platform[:3] == 'win':
        res = os.startfile(filename)
    elif sys.platform == 'darwin':
        res = os.system('open %s' % filename)
    elif sys.platform[:5] == 'linux':
        for c in ['gnome-open', 'kde-open', 'exo-open']:
            res = os.system('%s %s 2>/dev/null' % (c, filename))
            if res:
                break


def aghelp():
    helpfile = os.path.join(os.path.dirname(__file__), 'astrogrid.chm')
    open(helpfile)