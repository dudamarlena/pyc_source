# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/show_subcmd/__demo_helper__.py
# Compiled at: 2013-03-18 05:57:53
import os, sys
from import_relative import import_relative

def get_name():
    """Get the name caller's caller.
    NB: f_code.co_filenames and thus this code kind of broken for
    zip'ed eggs circa Jan 2009
    """
    caller = sys._getframe(2)
    filename = caller.f_code.co_filename
    filename = os.path.normcase(os.path.basename(filename))
    return os.path.splitext(filename)[0]


def demo_setup():
    Mmock = import_relative('mock', '..')
    Mshow = import_relative('show', '..')
    Mdebugger = import_relative('debugger', '....')
    (d, cp) = Mmock.dbg_setup()
    mgr = Mshow.ShowCommand(cp)
    return mgr


def demo_run(subcmd):
    mgr = demo_setup()
    sub = subcmd(mgr)
    sub.name = get_name()
    sub.run([])
    return sub