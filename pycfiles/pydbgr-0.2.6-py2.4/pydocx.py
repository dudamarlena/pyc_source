# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/pydocx.py
# Compiled at: 2013-01-12 00:47:14
import os, sys
sys_path_save = sys.path
realpath = lambda p: os.path.realpath(os.path.normcase(os.path.dirname(os.path.abspath(p))))
my_dir = realpath(__file__)
sys.path = [ p for p in sys.path if p != '' if realpath(p) != my_dir ]
Mpydoc = __import__('pydoc')
sys.path = sys_path_save
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')

class PyDocCommand(Mbase_cmd.DebuggerCommand):
    """**pydocx** *name* ...

Show pydoc documentation on something. *name* may be the name of a
Python keyword, topic, function, module, or package, or a dotted
reference to a class or function within a module or module in a
package.  If *name* contains a '/', it is used as the path to a Python
source file to document. If name is *keywords*, *topics*, or
*modules*, a listing of these things is displayed.
"""
    __module__ = __name__
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = False
    short_help = 'Run pydoc'

    def run(self, args):
        sys_path_save = list(sys.path)
        sys_argv_save = list(sys.argv)
        sys.argv = ['pydoc'] + args[1:]
        Mpydoc.cli()
        sys.argv = sys_argv_save
        sys.path = sys_path_save
        return False


if __name__ == '__main__':
    mock = import_relative('mock')
    (d, cp) = mock.dbg_setup()
    command = PyDocCommand(cp)