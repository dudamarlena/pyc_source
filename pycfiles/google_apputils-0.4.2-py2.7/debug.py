# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/google/apputils/debug.py
# Compiled at: 2015-02-20 20:25:16
"""Import this module to add a hook to call pdb on uncaught exceptions.

To enable this, do the following in your top-level application:

import google.apputils.debug

and then in your main():

google.apputils.debug.Init()

Then run your program with --pdb.
"""
import sys, gflags as flags
flags.DEFINE_boolean('pdb', 0, 'Drop into pdb on uncaught exceptions')
old_excepthook = None

def _DebugHandler(exc_class, value, tb):
    global old_excepthook
    if not flags.FLAGS.pdb or hasattr(sys, 'ps1') or not sys.stderr.isatty():
        old_excepthook(exc_class, value, tb)
    else:
        import traceback, pdb
        traceback.print_exception(exc_class, value, tb)
        sys.stdout.write('\n')
        pdb.pm()


def Init():
    global old_excepthook
    if old_excepthook is None:
        old_excepthook = sys.excepthook
        sys.excepthook = _DebugHandler
    return