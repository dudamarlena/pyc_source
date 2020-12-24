# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/pdef.py
# Compiled at: 2015-06-02 06:19:00
import inspect, os, types
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.lib import printing as Mprint

class PrintDefCommand(Mbase_cmd.DebuggerCommand):
    """**pdef** *obj*

Print the definition header for a callable object *obj*.
If the object is a class, print the constructor information.

See also:
---------

`pydocX`.
"""
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
        elif isinstance(type(obj), types.InstanceType):
            obj = obj.__call__
        output = Mprint.print_argspec(obj, obj_name)
        if output is None:
            self.errmsg('No definition header found for %s' % obj_name)
        else:
            self.msg(output)
        return


if __name__ == '__main__':
    from trepan import debugger
    d = debugger.Debugger()
    cp = d.core.processor
    cp.curframe = inspect.currentframe()
    command = PrintDefCommand(cp)
    command.run(['pdef', 'PrintDefCommand'])