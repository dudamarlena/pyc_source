# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iwm/recipe/bebopinstance/zope3scripts.py
# Compiled at: 2007-07-16 10:35:40
"""Zope 3 program entry points

The Zope 3 scripts, scriptzope, and debugzope are distributed
as templates, rather than as entry points. Here we provide entry-point
versions.

$Id: zope3scripts.py 70995 2006-10-30 12:13:58Z jim $
"""
import os, sys, zope.app.debug, zope.app.twisted.main

def zglobals(args):
    db = zope.app.twisted.main.debug(args)
    if 'PYTHONSTARTUP' in os.environ:
        execfile(os.environ['PYTHONSTARTUP'])
    app = zope.app.debug.Debugger.fromDatabase(db)
    return dict(app=app, debugger=app, root=app.root(), __name__='__main__')


def script(args):
    globs = zglobals(args[:2])
    sys.argv[:] = args[2:]
    globs['__file__'] = sys.argv[0]
    execfile(sys.argv[0], globs)
    sys.exit()


banner = 'Welcome to the Zope 3 "debugger".\nThe application root object is available as the root variable.\nA Zope debugger instance is available as the debugger (aka app) variable.\n'

def debug(args):
    globs = zglobals(args)
    import code
    code.interact(banner=banner, local=globs)