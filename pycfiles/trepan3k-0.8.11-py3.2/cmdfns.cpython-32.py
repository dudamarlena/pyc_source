# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/cmdfns.py
# Compiled at: 2018-03-11 10:22:50
""" Common command-parsing routines such as check command argument
counts, to parse a string for an integer, or check a string for an
on/off setting value.
"""
import os, sys, tempfile, pyficache
from xdis import IS_PYPY

def source_tempfile_remap(prefix, text):
    fd = tempfile.NamedTemporaryFile(suffix='.py', prefix=prefix, delete=False)
    with fd:
        fd.write(bytes(text, 'UTF-8'))
        fd.close()
    return fd.name


def deparse_fn(code):
    try:
        from uncompyle6.semanitcs.linemap import deparse_code_with_fragments_and_map as deparse_code
    except ImportError:
        return

    sys_version = sys.version[:5]
    try:
        float_version = py_str2float(sys_version)
        deparsed = deparse_code(float_version, code, is_pypy=IS_PYPY)
        return deparsed
    except:
        raise

    return


def deparse_getline(code, filename, line_number, opts):
    deparsed = deparse_fn(code)
    text = deparsed.text.strip()
    if text:
        prefix = os.path.basename(filename) + '_'
        remapped_filename = source_tempfile_remap(prefix, text)
        lines = text.split('\n')
        first_line = code.co_firstlineno
        linemap = [(line_no, deparsed.source_linemap[line_no]) for line_no in sorted(deparsed.source_linemap.keys())]
        print('XXXX', linemap)
        pyficache.remap_file_lines(filename, remapped_filename, linemap)
        return (
         remapped_filename, pyficache.getline(filename, line_number, opts))
    else:
        return (None, None)


def get_an_int(errmsg, arg, msg_on_error, min_value=None, max_value=None):
    """Another get_int() routine, this one simpler and less stylized
    than get_int(). We eval arg return it as an integer value or
    None if there was an error in parsing this.
    """
    ret_value = None
    if arg:
        try:
            ret_value = int(eval(arg))
        except (SyntaxError, NameError, ValueError):
            if errmsg:
                errmsg(msg_on_error)
            else:
                errmsg('Expecting an integer, got: %s.' % str(arg))
            return

    if min_value and ret_value < min_value:
        errmsg('Expecting integer value to be at least %d, got: %d.' % (
         min_value, ret_value))
        return
    else:
        if max_value and ret_value > max_value:
            errmsg('Expecting integer value to be at most %d, got: %d.' % (
             max_value, ret_value))
            return
        return ret_value


def get_int(errmsg, arg, default=1, cmdname=None):
    """If arg is an int, use that otherwise take default."""
    if arg:
        try:
            default = int(eval(arg))
        except (SyntaxError, NameError, ValueError):
            if cmdname:
                errmsg("Command '%s' expects an integer; got: %s." % (
                 cmdname, str(arg)))
            else:
                errmsg('Expecting an integer, got: %s.' % str(arg))
            raise ValueError

    return default


def get_onoff(errmsg, arg, default=None, print_error=True):
    """Return True if arg is 'on' or 1 and False arg is 'off' or 0.
    Any other value is raises ValueError."""
    if not arg:
        if default is None:
            if print_error:
                errmsg("Expecting 'on', 1, 'off', or 0. Got nothing.")
            raise ValueError
        return default
    else:
        if arg == '1' or arg == 'on':
            return True
        if arg == '0' or arg == 'off':
            return False
        if print_error:
            errmsg("Expecting 'on', 1, 'off', or 0. Got: %s." % str(arg))
        raise ValueError
        return


def get_val(curframe, errmsg, arg):
    try:
        return eval(arg, curframe.f_globals, curframe.f_locals)
    except:
        t, v = sys.exc_info()[:2]
        if isinstance(t, str):
            exc_type_name = t
        else:
            exc_type_name = t.__name__
        errmsg(str('%s: %s' % (exc_type_name, arg)))
        raise


def run_set_bool(obj, args):
    """set a Boolean-valued debugger setting. 'obj' is a generally a
    subcommand that has 'name' and 'debugger.settings' attributes"""
    try:
        if 0 == len(args):
            args = [
             'on']
        obj.debugger.settings[obj.name] = get_onoff(obj.errmsg, args[0])
    except ValueError:
        pass


def run_set_int(obj, arg, msg_on_error, min_value=None, max_value=None):
    """set an Integer-valued debugger setting. 'obj' is a generally a
    subcommand that has 'name' and 'debugger.settings' attributes"""
    if '' == arg.strip():
        obj.errmsg('You need to supply a number.')
        return
    obj.debugger.settings[obj.name] = get_an_int(obj.errmsg, arg, msg_on_error, min_value, max_value)
    return obj.debugger.settings[obj.name]


def run_show_bool(obj, what=None):
    """Generic subcommand showing a boolean-valued debugger setting.
    'obj' is generally a subcommand that has 'name' and
    'debugger.setting' attributes."""
    val = show_onoff(obj.debugger.settings[obj.name])
    if not what:
        what = obj.name
    return obj.msg('%s is %s.' % (what, val))


def run_show_int(obj, what=None):
    """Generic subcommand integer value display"""
    val = obj.debugger.settings[obj.name]
    if not what:
        what = obj.name
    return obj.msg('%s is %d.' % (what, val))


def show_onoff(b):
    """Return 'on' for True and 'off' for False, and ?? for anything
    else."""
    if not isinstance(b, bool):
        return '??'
    if b:
        return 'on'
    return 'off'


def run_show_val(obj, name):
    """Generic subcommand value display"""
    val = obj.debugger.settings[obj.name]
    obj.msg('%s is %s.' % (obj.name, obj.cmd.proc._saferepr(val)))
    return False


def want_different_line(cmd, default):
    if cmd[(-1)] == '-':
        return False
    if cmd[(-1)] == '+':
        return True
    return default


if __name__ == '__main__':

    def errmsg(msg):
        print('** %s' % msg)


    def msg(m):
        print(m)


    print(get_int(errmsg, '1+2'))
    print(get_int(errmsg, None))
    print(get_an_int(errmsg, '6*1', '6*1 is okay'))
    print(get_an_int(errmsg, '0', '0 is too small', 1))
    print(get_an_int(errmsg, '5+a', '5+a is no good'))
    try:
        get_int(errmsg, 'pi')
    except ValueError:
        print("Good - 'pi' is not an integer")

    import inspect
    curframe = inspect.currentframe()
    print(want_different_line('s+ %s', False))
    print(want_different_line('s-', True))
    print(want_different_line('s', False))
    print(want_different_line('s', True))
    print(want_different_line('s', True))