# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/pdef.py
# Compiled at: 2018-02-01 07:53:21
# Size of source mod 2**32: 2308 bytes
import inspect, os, types
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import printing as Mprint

class PrintDefCommand(Mbase_cmd.DebuggerCommand):
    __doc__ = '**pdef** *obj*\n\nPrint the definition header for a callable object *obj*.\nIf the object is a class, print the constructor information.\n\nSee also:\n---------\n\n`pydocX`.\n'
    category = 'data'
    min_args = 1
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print the definition header for a callable object'

    def run(self, args):
        if len(args) != 2:
            return
        else:
            obj_name = args[1]
            try:
                obj = self.proc.eval(obj_name)
            except:
                return

            if not callable(obj):
                self.errmsg('Object %s is not callable.' % obj_name)
                return
            if inspect.isclass(obj):
                self.msg('Class constructor information:')
                obj = obj.__init__
            output = Mprint.print_argspec(obj, obj_name)
            if output is None:
                self.errmsg('No definition header found for %s' % obj_name)
            else:
                self.msg(output)
            return


if __name__ == '__main__':
    from trepan import debugger
    d = debugger.Trepan()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = PrintDefCommand(cp)
    command.run(['pdef', 'PrintDefCommand'])