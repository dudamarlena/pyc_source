# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pydbgr/lib/stack.py
# Compiled at: 2013-03-24 09:32:15
__doc__ = ' Functions for working with Python frames'
import re, types
from import_relative import import_relative
Mbytecode = import_relative('lib.bytecode', '...pydbgr')
Mprint = import_relative('lib.print', '...pydbgr')
Mformat = import_relative('lib.format', '...pydbgr')
format_token = Mformat.format_token

def count_frames(frame, count_start=0):
    """Return a count of the number of frames"""
    count = -count_start
    while frame:
        count += 1
        frame = frame.f_back

    return count


import repr as Mrepr, inspect
_re_pseudo_file = re.compile('^<.+>')

def format_stack_entry(dbg_obj, frame_lineno, lprefix=': ', include_location=True, color='plain'):
    """Format and return a stack entry gdb-style.
    Note: lprefix is not used. It is kept for compatibility.
    """
    (frame, lineno) = frame_lineno
    filename = frame2file(dbg_obj.core, frame)
    s = ''
    if frame.f_code.co_name:
        funcname = frame.f_code.co_name
    else:
        funcname = '<lambda>'
    s = format_token(Mformat.Function, funcname, highlight=color)
    (args, varargs, varkw, local_vars) = inspect.getargvalues(frame)
    if '<module>' == funcname:
        if ([], None, None) == (args, varargs, varkw):
            is_module = True
            if is_exec_stmt(frame):
                fn_name = format_token(Mformat.Function, 'exec', highlight=color)
                s += ' %s()' % format_token(Mformat.Function, fn_name, highlight=color)
            else:
                fn_name = get_call_function_name(frame, color=color)
                if fn_name:
                    s += ' %s()' % format_token(Mformat.Function, fn_name, highlight=color)
        else:
            is_module = False
            parms = inspect.formatargvalues(args, varargs, varkw, local_vars)
            maxargstrsize = dbg_obj.settings['maxargstrsize']
            if len(parms) >= maxargstrsize:
                parms = '%s...)' % parms[0:maxargstrsize]
            s += parms
        if len(s) >= 35:
            s += '\n    '
        if '__return__' in frame.f_locals:
            rv = frame.f_locals['__return__']
            s += '->'
            s += format_token(Mformat.Return, Mrepr.repr(rv), highlight=color)
        if include_location:
            is_pseudo_file = _re_pseudo_file.match(filename)
            add_quotes_around_file = not is_pseudo_file
            if is_module:
                if not is_exec_stmt(frame) and not is_pseudo_file:
                    s += ' file'
            if s == '?()':
                if is_exec_stmt(frame):
                    s = 'in exec'
                else:
                    s = is_pseudo_file or 'in file'
        elif not is_pseudo_file:
            s += ' called from file'
        if add_quotes_around_file:
            filename = "'%s'" % filename
        s += ' %s at line %s' % (format_token(Mformat.Filename, filename, highlight=color), format_token(Mformat.LineNumber, '%r' % lineno, highlight=color))
    return s


def frame2file(core_obj, frame):
    return core_obj.filename(core_obj.canonic_filename(frame))


def is_exec_stmt(frame):
    """Return True if we are looking at an exec statement"""
    return hasattr(frame, 'f_back') and frame.f_back is not None and Mbytecode.op_at_frame(frame.f_back) == 'EXEC_STMT'


import dis

def get_call_function_name(frame, color='plain'):
    """If f_back is looking at a call function, return
    the name for it. Otherwise return None"""
    f_back = frame.f_back
    if not f_back:
        return
    if 'CALL_FUNCTION' != Mbytecode.op_at_frame(f_back):
        return
    co = f_back.f_code
    code = co.co_code
    linestarts = dict(dis.findlinestarts(co))
    inst = f_back.f_lasti
    while inst >= 0:
        if inst in linestarts:
            inst += 1
            oparg = ord(code[inst]) + (ord(code[(inst + 1)]) << 8)
            return format_token(Mformat.Function, co.co_names[oparg], highlight=color)
        inst -= 1

    return


def print_stack_entry(proc_obj, i_stack, color='plain'):
    frame_lineno = proc_obj.stack[(len(proc_obj.stack) - i_stack - 1)]
    (frame, lineno) = frame_lineno
    if frame is proc_obj.curframe:
        proc_obj.intf[(-1)].msg_nocr(format_token(Mformat.Arrow, '->', highlight=color))
    else:
        proc_obj.intf[(-1)].msg_nocr('##')
    proc_obj.intf[(-1)].msg('%d %s' % (i_stack, format_stack_entry(proc_obj.debugger, frame_lineno, color=color)))


def print_stack_trace(proc_obj, count=None, color='plain'):
    """Print count entries of the stack trace"""
    if count is None:
        n = len(proc_obj.stack)
    else:
        n = min(len(proc_obj.stack), count)
    try:
        for i in range(n):
            print_stack_entry(proc_obj, i, color=color)

    except KeyboardInterrupt:
        pass

    return


def print_dict(s, obj, title):
    if hasattr(obj, '__dict__'):
        d = obj.__dict__
        if type(d) == types.DictType or type(d) == types.DictProxyType:
            keys = list(d.keys())
            if len(keys) == 0:
                s += '\n  No %s' % title
            else:
                s += '\n  %s:\n' % title
            keys.sort()
            for key in keys:
                s += "    '%s':\t%s\n" % (key, d[key])

    return s


def eval_print_obj(arg, frame, format=None, short=False):
    """Return a string representation of an object """
    try:
        if not frame:
            val = eval(arg, None, None)
        else:
            val = eval(arg, frame.f_globals, frame.f_locals)
    except:
        return 'No symbol "' + arg + '" in current context.'

    return print_obj(arg, val, format, short)


def print_obj(arg, val, format=None, short=False):
    """Return a string representation of an object """
    what = arg
    if format:
        what = format + ' ' + arg
        val = Mprint.printf(val, format)
    s = '%s = %s' % (what, val)
    if not short:
        s += '\n  type = %s' % type(val)
        s = print_dict(s, val, 'object variables')
        if hasattr(val, '__class__'):
            s = print_dict(s, val.__class__, 'class variables')
    return s


if __name__ == '__main__':

    class MockDebuggerCore:
        __module__ = __name__

        def canonic_filename(self, frame):
            return frame.f_code.co_filename

        def filename(self, name):
            return name


    class MockDebugger:
        __module__ = __name__

        def __init__(self):
            self.core = MockDebuggerCore()
            self.settings = {'maxargstrsize': 80}


    frame = inspect.currentframe()
    m = MockDebugger()
    print format_stack_entry(m, (frame, 10))
    print format_stack_entry(m, (frame, 10), color='dark')
    print 'frame count: %d' % count_frames(frame)
    print 'frame count: %d' % count_frames(frame.f_back)
    print 'frame count: %d' % count_frames(frame, 1)
    print 'def statement: x=5?: %s' % repr(Mbytecode.is_def_stmt('x=5', frame))
    print Mbytecode.is_def_stmt('def foo():', frame)

    def sqr(x):
        x * x


    def fn(x):
        frame = inspect.currentframe()
        print get_call_function_name(frame)


    print '=' * 30
    eval('fn(5)')
    print '=' * 30
    print print_obj('fn', fn)
    print '=' * 30
    print print_obj('len', len)
    print '=' * 30
    print print_obj('MockDebugger', MockDebugger)