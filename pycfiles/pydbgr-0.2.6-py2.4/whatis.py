# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/whatis.py
# Compiled at: 2013-03-17 23:10:25
import inspect, os, sys, types
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mstack = import_relative('stack', '...lib', 'pydbgr')
Mcmdfns = import_relative('cmdfns', '..', 'pydbgr')

class WhatisCommand(Mbase_cmd.DebuggerCommand):
    """**whatis** *arg*

Prints the type of the argument which can be a Python expression."""
    __module__ = __name__
    aliases = ()
    category = 'data'
    min_args = 0
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print data type of expression EXP'

    def run(self, args):
        arg = (' ').join(args[1:])
        try:
            if not self.proc.curframe:
                value = eval(arg, None, None)
            else:
                value = eval(arg, self.proc.curframe.f_globals, self.proc.curframe.f_locals)
        except:
            (t, v) = sys.exc_info()[:2]
            if type(t) == str:
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            if exc_type_name == 'NameError':
                self.errmsg('Name Error: %s' % arg)
            else:
                self.errmsg('%s: %s' % (exc_type_name, self.proc._saferepr(v)))
            return False

        if inspect.ismethod(value):
            self.msg('method %s%s' % (value.func_code.co_name, inspect.formatargspec(inspect.getargspec(value))))
            if inspect.getdoc(value):
                self.msg('%s:\n%s' % (value, inspect.getdoc(value)))
            return False
        elif inspect.isfunction(value):
            self.msg('function %s%s' % (value.func_code.co_name, inspect.formatargspec(inspect.getargspec(value))))
            if inspect.getdoc(value):
                self.msg('%s:\n%s' % (value, inspect.getdoc(value)))
            return False
        self.msg(type(value))
        return False


if __name__ == '__main__':
    Mcmdproc = import_relative('cmdproc', '..')
    Mmock = import_relative('mock')
    (d, cp) = Mmock.dbg_setup()
    command = WhatisCommand(cp)
    cp.curframe = inspect.currentframe()
    (cp.stack, cp.curindex) = Mcmdproc.get_stack(cp.curframe, None, None, cp)
    command.run(['whatis', 'cp'])
    command.run(['whatis', '5'])