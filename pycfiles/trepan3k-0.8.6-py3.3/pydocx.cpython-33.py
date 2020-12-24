# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/pydocx.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2489 bytes
import os, sys
sys_path_save = sys.path
realpath = lambda p: os.path.realpath(os.path.normcase(os.path.dirname(os.path.abspath(p))))
my_dir = realpath(__file__)
sys.path = [p for p in sys.path if p != '' and realpath(p) != my_dir]
Mpydoc = __import__('pydoc')
sys.path = sys_path_save
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class PyDocCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = "**pydocx** *name* ...\n\nShow pydoc documentation on something. *name* may be the name of a\nPython keyword, topic, function, module, or package, or a dotted\nreference to a class or function within a module or module in a\npackage.  If *name* contains a '/', it is used as the path to a Python\nsource file to document. If name is *keywords*, *topics*, or\n*modules*, a listing of these things is displayed.\n\nSee also:\n---------\n\n`whatis`\n"
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Run pydoc'
    complete = Mcomplete.complete_id_and_builtins

    def run(self, args):
        sys_path_save = list(sys.path)
        sys_argv_save = list(sys.argv)
        sys.argv = ['pydoc'] + args[1:]
        Mpydoc.cli()
        sys.argv = sys_argv_save
        sys.path = sys_path_save
        return False


if __name__ == '__main__':
    from trepan.processor.command import mock
    d, cp = mock.dbg_setup()
    command = PyDocCommand(cp)