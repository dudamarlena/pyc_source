# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/show_subcmd/__demo_helper__.py
# Compiled at: 2015-02-16 15:47:50
import os, sys

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
    from trepan.processor.command import mock as Mmock, show as Mshow
    (d, cp) = Mmock.dbg_setup()
    mgr = Mshow.ShowCommand(cp)
    return mgr


def demo_run(subcmd):
    mgr = demo_setup()
    sub = subcmd(mgr)
    sub.name = get_name()
    sub.run([])
    return sub