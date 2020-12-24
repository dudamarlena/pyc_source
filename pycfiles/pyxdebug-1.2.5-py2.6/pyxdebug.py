# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/pyxdebug.py
# Compiled at: 2011-11-30 05:54:53
import sys, os, time, inspect, re, linecache
from pprint import pformat
try:
    import resource
except ImportError:
    resource = None

import __builtin__
__version__ = '1.2.5'
__author__ = 'Yoshida Tetsuya'
__license__ = 'MIT License'
this_path = __name__
if __name__ == '__main__':
    this_path = __file__
this_path = os.path.splitext(os.path.abspath(this_path))[0]

class PyXdebug(object):

    def __init__(self):
        self.initialize()
        self.collect_imports = 1
        self.collect_params = 0
        self.collect_return = 0
        self.collect_assignments = 0

    def initialize(self):
        self.start_time = None
        self.start_gmtime = None
        self.end_gmtime = None
        self.call_depth = 0
        self.call_func_name = None
        self.late_dispatch = []
        self.result = []
        return

    def run_func(self, func, *args, **kwds):
        self.initialize()
        self.call_func_name = getattr(func, '__name__', None)
        return self._run(func, *args, **kwds)

    def run_statement(self, statement, globals_=None, locals_=None):
        self.initialize()
        if globals_ is None:
            import __main__
            globals_ = __main__.__dict__
        if locals_ is None:
            locals_ = inspect.currentframe().f_back.f_locals

        def exec_statement():
            exec statement in globals_, locals_

        return self._run(exec_statement)

    def run_file(self, script_path, globals_=None):
        self.initialize()
        if globals_ is None:
            globals_ = globals()
        return self._run(execfile, script_path, globals_)

    def _run(self, func, *args, **kwds):
        if not hasattr(func, '__call__'):
            raise PyXdebugError('func is not callable')
        import_hooked = False
        if self.collect_imports:
            import_hooked = True
            original_import = __builtin__.__import__
            original_reload = __builtin__.reload

            def __pyxdebug_import_hook(name, globals=None, locals=None, fromlist=None, **kwds):
                frame = inspect.currentframe()
                self.trace_import(frame, (name, fromlist))
                result = None
                try:
                    result = original_import(name, globals, locals, fromlist, **kwds)
                    return result
                finally:
                    self.trace_return(frame, result)

                return

            def __pyxdebug_reload_hook(module):
                frame = inspect.currentframe()
                self.trace_reload(frame, module)
                result = None
                try:
                    result = original_reload(module)
                    return result
                finally:
                    self.trace_return(frame, result)

                return

            __builtin__.__import__ = __pyxdebug_import_hook
            __builtin__.reload = __pyxdebug_reload_hook
        original_trace = sys.gettrace()
        sys.settrace(self.trace_dispatch)
        self.start_time = time.time()
        self.start_gmtime = time.gmtime()
        try:
            return func(*args, **kwds)
        finally:
            sys.settrace(original_trace)
            self.end_gmtime = time.gmtime()
            if import_hooked:
                __builtin__.__import__ = original_import
                __builtin__.reload = original_reload
            trace = FinishTrace(None, 0)
            trace.setvalue(self.start_time)
            self.result.append(trace)

        return

    def trace_dispatch(self, frame, event, arg):
        if frame.f_code.co_name in ('__pyxdebug_import_hook', '__pyxdebug_reload_hook'):
            return
        else:
            if os.path.splitext(os.path.abspath(frame.f_back.f_code.co_filename))[0] == this_path:
                if self.call_func_name is None or self.call_func_name != frame.f_code.co_name:
                    return
            if event[0:2] == 'c_':
                event = event[2:]
            frame = FrameWrap(frame)
            f_back = frame.f_back
            while f_back:
                if os.path.splitext(os.path.abspath(f_back.f_code.co_filename))[0] == this_path:
                    f_back = f_back.f_back
                else:
                    break

            frame.f_back = FrameWrap(f_back)
            if event == 'call':
                self.trace_call(frame, arg)
                if self.collect_assignments:
                    self.late_dispatch.append(None)
            elif event == 'return':
                if self.collect_assignments:
                    self.trace_line(frame, arg)
                    self.late_dispatch.pop()
                self.trace_return(frame, arg)
            elif event == 'line':
                if self.collect_assignments:
                    self.trace_line(frame, arg)
            return self.trace_dispatch

    def trace_call(self, frame, arg):
        trace = CallTrace(frame, self.call_depth)
        trace.setvalue(self.start_time, self.collect_params)
        self.result.append(trace)
        self.call_depth += 1

    def trace_return(self, frame, arg):
        self.call_depth -= 1
        if self.collect_return:
            trace = ReturnTrace(None, self.call_depth)
            trace.setvalue(arg)
            self.result.append(trace)
        return

    def trace_line(self, frame, arg):
        pre_frame = self.late_dispatch[(self.call_depth - 1)]
        self.late_dispatch[self.call_depth - 1] = frame
        if pre_frame:
            frame = FrameWrap(frame)
            frame.set_position(pre_frame)
            self._trace_line(frame)

    def _trace_line(self, frame):
        line = frame.get_line().strip()
        match = re.compile('^([^\\+\\-\\*/=]+)([\\+\\-\\*/]?=[^=])(.+)$').match(line)
        if match:
            varnames = match.group(1).strip()
            try:
                varnames = re.compile('^\\((.+)\\)$').match(varnames).group(1).strip()
            except:
                pass
            else:
                if re.compile('^(([a-zA-Z0-9_]+\\.)?[a-zA-Z0-9_]+)(\\s*,\\s*(([a-zA-Z0-9_]+\\.)?[a-zA-Z0-9_]+))*(\\s*,\\s*)?$').match(varnames):
                    varnames = re.compile('\\s*,\\s*').split(varnames)
                else:
                    varnames = None
                if varnames:
                    for varname in varnames:
                        value = get_frame_var(frame, varname)
                        trace = AssignmentTrace(frame, self.call_depth)
                        trace.setvalue(varname, value)
                        self.result.append(trace)

        return

    def trace_import(self, frame, arg):
        trace = ImportTrace(frame, self.call_depth)
        trace.setvalue(arg[0], arg[1], self.start_time)
        self.result.append(trace)
        self.call_depth += 1

    def trace_reload(self, frame, arg):
        trace = ReloadTrace(frame, self.call_depth)
        trace.setvalue(arg, self.start_time)
        self.result.append(trace)
        self.call_depth += 1

    def get_result(self):
        if self.end_gmtime is None:
            raise PyXdebugError('PyXdebug has not run yet')
        result = 'TRACE START [%s]\n' % time.strftime('%Y-%m-%d %H:%M:%S', self.start_gmtime)
        result += ('\n').join([ o.get_result() for o in self.result ])
        result += '\nTRACE END   [%s]\n\n' % time.strftime('%Y-%m-%d %H:%M:%S', self.end_gmtime)
        return result


class BaseTrace(object):

    def __init__(self, callee, call_depth):
        if callee:
            self.callee = callee
            self.caller = callee.f_back
        else:
            self.callee = None
            self.caller = None
        self.call_depth = call_depth
        return


class CallTrace(BaseTrace):

    def __init__(self, callee, call_depth):
        super(CallTrace, self).__init__(callee, call_depth)
        self.time = None
        self.collect_params = None
        self.memory = None
        return

    def setvalue(self, start_time, collect_params=False):
        self.time = time.time() - start_time
        self.collect_params = collect_params
        if resource is not None:
            self.memory = resource.getrusage(resource.RUSAGE_SELF).ru_minflt
        return

    def callee_name(self):
        return get_method_name(self.callee)

    def caller_filename(self):
        return self.caller.f_code.co_filename

    def caller_lineno(self):
        return self.caller.f_lineno

    def get_params(self):
        params = []
        if self.collect_params:
            arginfo = inspect.getargvalues(self.callee)
            for key in arginfo.args:
                if isinstance(key, basestring):
                    params.append((key, arginfo.locals.get(key)))
                elif isinstance(key, list):
                    keys = key
                    for key in keys:
                        params.append((key, arginfo.locals.get(key)))

            if arginfo.varargs:
                for value in arginfo.locals[arginfo.varargs]:
                    params.append((None, value))

            if arginfo.keywords:
                kwds = arginfo.locals.get(arginfo.keywords)
                for (key, value) in kwds.iteritems():
                    params.append((key, value))

        return params

    def get_params_str(self):
        params_str = []
        params = self.get_params()
        for (key, value) in params:
            prefix = ''
            if key is not None:
                prefix = '%s=' % key
            param_str = '%s%s' % (prefix, pformat(value))
            params_str.append(param_str)

        return (', ').join(params_str)

    def get_result(self):
        sp = '  ' * self.call_depth
        params = self.get_params_str()
        return '%10.4f %10d   %s-> %s(%s) %s:%d' % (self.time or 0.0, self.memory or 0, sp, self.callee_name(), params, self.caller_filename(), self.caller_lineno())


class ReturnTrace(BaseTrace):

    def setvalue(self, value):
        self.value = value

    def get_result(self):
        sp = ' ' * 24 + '  ' * self.call_depth
        return '%s>=> %s' % (sp, pformat(self.value))


class AssignmentTrace(BaseTrace):

    def __init__(self, callee, call_depth):
        super(AssignmentTrace, self).__init__(callee, call_depth)
        self.varname = None
        self.value = None
        return

    def setvalue(self, varname, value):
        self.varname = varname
        self.value = value

    def get_result(self):
        sp = ' ' * 24 + '  ' * self.call_depth
        filename = self.callee.f_code.co_filename
        lineno = self.callee.f_lineno
        return '%s=> %s = %s %s:%d' % (sp, self.varname, pformat(self.value), filename, lineno)


class ImportTrace(CallTrace):

    def __init__(self, callee, call_depth):
        super(ImportTrace, self).__init__(callee, call_depth)
        self.name = None
        self.fromlist = None
        return

    def setvalue(self, name, fromlist, start_time):
        super(ImportTrace, self).setvalue(start_time)
        self.name = name
        self.fromlist = fromlist

    def get_import_str(self):
        if self.fromlist:
            return 'from %s import %s' % (self.name, (', ').join(self.fromlist))
        else:
            return 'import %s' % (self.name,)

    def get_result(self):
        sp = '  ' * self.call_depth
        imp = self.get_import_str()
        return '%10.4f %10d   %s-> %s %s:%d' % (self.time or 0.0, self.memory or 0, sp, imp, self.caller_filename(), self.caller_lineno())


class ReloadTrace(CallTrace):

    def __init__(self, callee, call_depth):
        super(ReloadTrace, self).__init__(callee, call_depth)
        self.module = None
        return

    def setvalue(self, module, start_time):
        super(ReloadTrace, self).setvalue(start_time)
        self.module = getattr(module, '__name__', None)
        return

    def get_result(self):
        sp = '  ' * self.call_depth
        return '%10.4f %10d   %s-> reload(%s) %s:%d' % (self.time or 0.0, self.memory or 0, sp, self.module, self.caller_filename(), self.caller_lineno())


class FinishTrace(CallTrace):

    def setvalue(self, start_time):
        super(FinishTrace, self).setvalue(start_time)

    def get_result(self):
        return '%10.4f %10d' % (self.time or 0.0, self.memory or 0)


class LogTrace(BaseTrace):

    def __init__(self, callee, call_depth):
        super(LogTrace, self).__init__(callee, call_depth)
        self.message = None
        return

    def setvalue(self, message):
        self.message = message

    def get_result(self):
        sp = ' ' * 24 + '  ' * self.call_depth
        return '%s*> %s' % (sp, self.message)


class PyXdebugError(Exception):
    pass


def get_method_class(frame):
    arginfo = inspect.getargvalues(frame)
    obj = None
    if arginfo.args and len(arginfo.args):
        key = arginfo.args[0]
        if isinstance(key, (list, tuple)):
            return
        obj = arginfo.locals.get(key)
    elif arginfo.varargs and len(arginfo.locals[arginfo.varargs]):
        obj = arginfo.locals[arginfo.varargs][0]
    elif arginfo.keywords:
        kwds = arginfo.locals.get(arginfo.keywords)
        if 'self' in kwds:
            obj = kwds['self']
        elif 'cls' in arginfo.keywords:
            obj = kwds['cls']
    if obj is not None:
        if not inspect.isclass(obj):
            obj = obj.__class__
        if not inspect.isclass(obj) or str(obj).startswith("<type '"):
            obj = None
        method = getattr(obj, frame.f_code.co_name, None)
        if not inspect.ismethod(method) and not inspect.isfunction(method):
            obj = None
    return obj


def get_method_name(frame):
    method_class = get_method_class(frame)
    classname = ''
    if method_class is not None:
        classname = str(method_class)
        try:
            classname = re.compile("<class '([^']+)'>").match(classname).group(1)
        except:
            pass

    if len(classname):
        methodname = classname + '.' + frame.f_code.co_name
    else:
        methodname = frame.f_code.co_name
    return methodname


def get_frame_var(frame, varname):
    objectname = None
    attrname = None
    value = None
    try:
        (objectname, attrname) = varname.split('.')
    except:
        pass

    if objectname:
        object = frame.f_locals.get(objectname, None)
        value = getattr(object, attrname, None)
    else:
        value = frame.f_locals.get(varname, None)
    return value


class FrameWrap(object):

    def __init__(self, frame):
        keys = ('f_back', 'f_builtins', 'f_code', 'f_exc_traceback', 'f_exc_type',
                'f_exc_value', 'f_globals', 'f_lasti', 'f_lineno', 'f_locals', 'f_restricted',
                'f_trace')
        for key in keys:
            value = getattr(frame, key, None)
            setattr(self, key, value)

        return

    def get_line(self):
        filename = self.f_code.co_filename
        lineno = self.f_lineno
        return linecache.getline(filename, lineno)

    def set_position(self, other):
        self.f_code = getattr(other, 'f_code', None)
        self.f_lineno = getattr(other, 'f_lineno', None)
        return


def main():
    from optparse import OptionParser, OptionValueError

    def action_output(option, opt_str, value, parser, *args, **kwargs):
        rargs = parser.rargs
        arg = rargs[0] if len(rargs) else '---'
        if arg[:2] == '--' and len(arg) > 2 or arg[:1] == '-' and len(arg) > 1 and arg[1] != '-':
            raise OptionValueError('%s option requires an argument' % opt_str)
        del rargs[0]
        arg_l = arg.lower()
        if arg_l == 'stdout':
            value = sys.stdout
        else:
            if arg_l == 'stderr':
                value = sys.stderr
            else:
                try:
                    value = open(arg, 'a')
                except IOError, e:
                    raise OptionValueError(str(e))

            setattr(parser.values, option.dest, value)

    def action_int(option, opt_str, value, parser, *args, **kwargs):
        rargs = parser.rargs
        arg = rargs[0] if len(rargs) else '---'
        if arg[:2] == '--' and len(arg) > 2 or arg[:1] == '-' and len(arg) > 1 and arg[1] != '-':
            raise OptionValueError('%s option requires an argument' % opt_str)
        value = arg
        del rargs[0]
        try:
            value = int(value)
        except:
            raise OptionValueError('%s option requires an integer value' % opt_str)

        setattr(parser.values, option.dest, value)

    usage = 'pyxdebug.py [-o output_file_path] [-i collect_import] [-p collect_params] [-r collect_return] [-a collect_assignments] script_path [args ...]'
    parser = OptionParser(usage=usage)
    parser.allow_interspersed_args = False
    parser.add_option('-o', '--outfile', action='callback', callback=action_output, dest='outfile', help='Save stats to <outfile>', default=sys.stdout)
    parser.add_option('-i', '--collect_imports', action='callback', callback=action_int, dest='collect_imports', help='This setting, defaulting to 1, controls whether PyXdebug should write the filename used in import or reload to the trace files.', default=1)
    parser.add_option('-p', '--collect_params', action='callback', callback=action_int, dest='collect_params', help='This setting, defaulting to 0, controls whether PyXdebug should collect the parameters passed to functions when a function call is recorded in either the function trace or the stack trace.', default=0)
    parser.add_option('-r', '--collect_return', action='callback', callback=action_int, dest='collect_return', help='This setting, defaulting to 0, controls whether PyXdebug should write the return value of function calls to the trace files.', default=0)
    parser.add_option('-a', '--collect_assignments', action='callback', callback=action_int, dest='collect_assignments', help='This setting, defaulting to 0, controls whether PyXdebug should add variable assignments to function traces.', default=0)
    (options, args) = parser.parse_args()
    if len(args) == 0 or os.path.splitext(os.path.abspath(args[0]))[0] == this_path:
        parser.print_help()
        sys.exit(2)
    script_path = args[0]
    sys.argv[:] = args
    xd = PyXdebug()
    xd.collect_imports = options.collect_imports
    xd.collect_params = options.collect_params
    xd.collect_return = options.collect_return
    xd.collect_assignments = options.collect_assignments
    xd.run_file(script_path)
    result = xd.get_result()
    options.outfile.write(result)


if __name__ == '__main__':
    main()