# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/whatis.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 4513 bytes
import inspect, os, sys, types
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import complete as Mcomplete

class WhatisCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**whatis** *arg*\n\nPrints the information argument which can be a Python expression.\n\nWhen possible, we give information about:\n\n* type of argument\n\n* doc string for the argument (if a module, class, or function)\n\n* comments around the definition of the argument (module)\n\n* the module it was defined in\n\n* where the argument was defined\n\nWe get this most of this information via the *inspect* module.\n\nSee also:\n--------\n\n`pydocx`, the *inspect* module.'
    aliases = ()
    category = 'data'
    min_args = 1
    max_args = None
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print data type of expression EXP'
    complete = Mcomplete.complete_id_and_builtins

    def run(self, args):
        proc = self.proc
        arg = proc.cmd_argstr
        try:
            if not proc.curframe:
                value = eval(arg, None, None)
            else:
                value = eval(arg, proc.curframe.f_globals, proc.curframe.f_locals)
        except:
            t, v = sys.exc_info()[:2]
            if type(t) == str:
                exc_type_name = t
            else:
                exc_type_name = t.__name__
            if exc_type_name == 'NameError':
                self.errmsg('Name Error: %s' % arg)
            else:
                self.errmsg('%s: %s' % (exc_type_name, proc._saferepr(v)))
            return False

        self.section('What is for %s' % arg)
        get_doc = False
        if inspect.ismethod(value):
            get_doc = True
            self.msg('  method %s%s' % (
             value.__code__.co_name,
             inspect.formatargspec(inspect.getargspec(value))))
        else:
            if inspect.isfunction(value):
                get_doc = True
                self.msg('  function %s%s' % (
                 value.__code__.co_name, inspect.signature(value)))
            elif inspect.isabstract(value) or inspect.isbuiltin(value) or inspect.isclass(value) or inspect.isgeneratorfunction(value) or inspect.ismethoddescriptor(value):
                get_doc = True
        self.msg('  type: %s' % type(value))
        doc = inspect.getdoc(value)
        if get_doc:
            if doc:
                self.msg('  doc:\n%s' % doc)
        comments = inspect.getcomments(value)
        if comments:
            self.msg('  comments:\n%s' % comments)
        try:
            m = inspect.getmodule(value)
            if m:
                self.msg('  module:\t%s' % m)
        except:
            try:
                f = inspect.getfile(value)
                self.msg('  file: %s' % f)
            except:
                pass

        return False


if __name__ == '__main__':
    from trepan.processor import cmdproc as Mcmdproc
    from trepan.processor.command import mock as Mmock
    d, cp = Mmock.dbg_setup()
    command = WhatisCommand(cp)
    cp.curframe = inspect.currentframe()
    cp.stack, cp.curindex = Mcmdproc.get_stack(cp.curframe, None, None, cp)
    words = '5 1+2 thing len trepan os.path.basename WhatisCommand cp\n               __name__ Mmock Mbase_cmd.DebuggerCommand'.split()
    for thing in words:
        cp.cmd_argstr = thing
        command.run(['whatis', thing])
        print('----------')