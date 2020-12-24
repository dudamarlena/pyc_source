# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/processor/command/pdef.py
# Compiled at: 2013-01-10 07:29:09
import inspect, os, types
from import_relative import import_relative
Mbase_cmd = import_relative('base_cmd', top_name='pydbgr')
Mprint = import_relative('print', '...lib', 'pydbgr')

class PrintDefCommand(Mbase_cmd.DebuggerCommand):
    """**pdef** *obj*

Print the definition header for a callable object *obj*.
If the object is a class, print the constructor information.

See also `pydocX`."""
    __module__ = __name__
    category = 'data'
    min_args = 1
    max_args = 1
    name = os.path.basename(__file__).split('.')[0]
    need_stack = True
    short_help = 'Print the definition header for a callable object'

    def run(self, args):
        if len(args) != 2:
            return
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
        elif type(obj) is types.InstanceType:
            obj = obj.__call__
        output = Mprint.print_argspec(obj, obj_name)
        if output is None:
            self.errmsg('No definition header found for %s' % obj_name)
        else:
            self.msg(output)
        return


if __name__ == '__main__':
    cmdproc = import_relative('cmdproc', '..')
    debugger = import_relative('debugger', '...')
    d = debugger.Debugger()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = PrintDefCommand(cp)
    command.run(['pdef', 'import_relative'])
    command.run(['pdef', 'PrintDefCommand'])