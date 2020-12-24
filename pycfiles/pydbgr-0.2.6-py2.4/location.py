# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/bwprocessor/location.py
# Compiled at: 2013-03-24 09:33:03
""" Location routines"""
import pyficache, linecache, tempfile
from import_relative import import_relative, get_srcdir
Mstack = import_relative('stack', '..lib', 'pydbgr')

def format_location(proc_obj):
    """Show where we are. GUI's and front-end interfaces often
    use this to update displays. So it is helpful to make sure
    we give at least some place that's located in a file.      
    """
    i_stack = proc_obj.curindex
    if i_stack is None or proc_obj.stack is None:
        return False
    location = {}
    core_obj = proc_obj.core
    dbgr_obj = proc_obj.debugger
    remapped_file = None
    while i_stack >= 0:
        frame_lineno = proc_obj.stack[i_stack]
        i_stack -= 1
        (frame, lineno) = frame_lineno
        filename = Mstack.frame2file(core_obj, frame)
        location['filename'] = filename
        location['fn_name'] = frame.f_code.co_name
        location['lineno'] = lineno
        if '<string>' == filename and dbgr_obj.eval_string:
            remapped_file = filename
            filename = pyficache.unmap_file(filename)
            if '<string>' == filename:
                fd = tempfile.NamedTemporaryFile(suffix='.py', prefix='eval_string', delete=False)
                fd.write(dbgr_obj.eval_string)
                fd.close()
                pyficache.remap_file(fd.name, '<string>')
                filename = fd.name
        opts = {'reload_on_change': proc_obj.settings('reload'), 'output': 'plain'}
        line = pyficache.getline(filename, lineno, opts)
        if not line:
            line = linecache.getline(filename, lineno, proc_obj.curframe.f_globals)
        if line and len(line.strip()) != 0:
            location['text'] = line
        if '<string>' != filename:
            break

    return location


def print_location(proc_obj, event=None):
    response = proc_obj.response
    response['name'] = 'status'
    response['location'] = format_location(proc_obj)
    if event:
        response['event'] = event
        if event in ['return', 'exception']:
            val = proc_obj._saferepr(proc_obj.event_arg)
            event['arg'] = val
    proc_obj.intf[(-1)].msg(response)


if __name__ == '__main__':

    class MockDebugger:
        __module__ = __name__

        def __init__(self):
            self.eval_string = None
            return


    class MockProcessor:
        __module__ = __name__

        def __init__(self, core_obj):
            self.curindex = 0
            self.stack = []
            self.core = core_obj
            self.debugger = MockDebugger()
            self.opts = {'highlight': 'plain', 'reload': False}

        def settings(self, key):
            return self.opts[key]


    class MockCore:
        __module__ = __name__

        def filename(self, fn):
            return fn

        def canonic_filename(self, frame):
            return frame.f_code.co_filename


    core = MockCore()
    cmdproc = MockProcessor(core)
    import sys
    cmdproc.curframe = cmdproc.frame = sys._getframe()
    cmdproc.stack.append((sys._getframe(), 10))
    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(format_location(cmdproc))

    def test(cmdproc, pp):
        cmdproc.stack[0:0] = [
         (
          sys._getframe(1), 1)]
        pp.pprint(format_location(cmdproc))


    eval('test(cmdproc, pp)')
    cmdproc.debugger.eval_string = 'Fooled you!'
    eval('test(cmdproc, pp)')