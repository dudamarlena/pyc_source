# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/codelens/pg_logger.py
# Compiled at: 2020-03-27 10:52:12
# Size of source mod 2**32: 59776 bytes
import sys, bdb, re, traceback, types
is_python3 = sys.version_info[0] == 3
if is_python3:
    import io as StringIO, io
else:
    import StringIO
import runestone.codelens.pg_encoder as pg_encoder
MAX_EXECUTED_LINES = 1000
DEBUG = True
BREAKPOINT_STR = '#break'
CLASS_RE = re.compile('class\\s+')
try:
    import resource
    resource_module_loaded = True
except ImportError:
    resource_module_loaded = False

class NullDevice:

    def write(self, s):
        pass


__html__ = None

def setHTML(htmlStr):
    global __html__
    __html__ = htmlStr


__css__ = None

def setCSS(cssStr):
    global __css__
    __css__ = cssStr


__js__ = None

def setJS(jsStr):
    global __js__
    __js__ = jsStr


if type(__builtins__) is dict:
    BUILTIN_IMPORT = __builtins__['__import__']
else:
    assert type(__builtins__) is types.ModuleType
    BUILTIN_IMPORT = __builtins__.__import__
ALLOWED_STDLIB_MODULE_IMPORTS = ('math', 'random', 'time', 'datetime', 'functools',
                                 'itertools', 'operator', 'string', 'collections',
                                 're', 'json', 'heapq', 'bisect', 'copy', 'hashlib')
OTHER_STDLIB_WHITELIST = ('StringIO', 'io')
CUSTOM_MODULE_IMPORTS = ('runestone.codelens.callback_module', 'runestone.codelens.ttt_module',
                         'runestone.codelens.html_module', 'runestone.codelens.htmlexample_module',
                         'runestone.codelens.matrix', 'runestone.codelens.htmlFrame')
for m in ALLOWED_STDLIB_MODULE_IMPORTS + CUSTOM_MODULE_IMPORTS:
    __import__(m)

def __restricted_import__(*args):
    args = [e for e in args if type(e) is str]
    if args[0] in ALLOWED_STDLIB_MODULE_IMPORTS + CUSTOM_MODULE_IMPORTS + OTHER_STDLIB_WHITELIST:
        imported_mod = BUILTIN_IMPORT(*args)
        if args[0] in CUSTOM_MODULE_IMPORTS:
            setattr(imported_mod, 'setHTML', setHTML)
            setattr(imported_mod, 'setCSS', setCSS)
            setattr(imported_mod, 'setJS', setJS)
        for mod in ('os', 'sys', 'posix', 'gc'):
            if hasattr(imported_mod, mod):
                delattr(imported_mod, mod)

        return imported_mod
    raise ImportError('{0} not supported'.format(args[0]))


import random
random.seed(0)
input_string_queue = []

def open_wrapper(*args):
    if is_python3:
        raise Exception('open() is not supported by Python Tutor.\nInstead use io.StringIO() to simulate a file.\nHere is an example: http://goo.gl/uNvBGl')
    else:
        raise Exception('open() is not supported by Python Tutor.\nInstead use StringIO.StringIO() to simulate a file.\nHere is an example: http://goo.gl/Q9xQ4p')


def create_banned_builtins_wrapper(fn_name):

    def err_func(*args):
        raise Exception("'" + fn_name + "' is not supported by Python Tutor.")

    return err_func


class RawInputException(Exception):
    pass


def raw_input_wrapper(prompt=''):
    global input_string_queue
    if input_string_queue:
        input_str = input_string_queue.pop(0)
        sys.stdout.write(str(prompt))
        sys.stdout.write(input_str + '\n')
        return input_str
    raise RawInputException(str(prompt))


def python2_input_wrapper(prompt=''):
    if input_string_queue:
        input_str = input_string_queue.pop(0)
        sys.stdout.write(str(prompt))
        sys.stdout.write(input_str + '\n')
        return eval(input_str)
    raise RawInputException(str(prompt))


class MouseInputException(Exception):
    pass


def mouse_input_wrapper(prompt=''):
    if input_string_queue:
        return input_string_queue.pop(0)
    raise MouseInputException(prompt)


BANNED_BUILTINS = [
 'reload',
 'open',
 'compile',
 'file',
 'eval',
 'exec',
 'execfile',
 'exit',
 'quit',
 'help',
 'dir',
 'globals',
 'locals',
 'vars']
IGNORE_VARS = set(('__user_stdout__', '__OPT_toplevel__', '__builtins__', '__name__',
                   '__exception__', '__doc__', '__package__'))

def get_user_stdout(frame):
    my_user_stdout = frame.f_globals['__user_stdout__']
    if not is_python3:
        my_user_stdout.buflist = [e.decode('utf-8', 'replace') if type(e) is str else e for e in my_user_stdout.buflist]
    return my_user_stdout.getvalue()


def get_user_globals(frame, at_global_scope=False):
    d = filter_var_dict(frame.f_globals)
    if not is_python3:
        if hasattr(frame, 'f_valuestack'):
            for i, e in enumerate([e for e in frame.f_valuestack if type(e) is list]):
                d['_tmp' + str(i + 1)] = e

    if '__return__' in d:
        del d['__return__']
    return d


def get_user_locals(frame):
    ret = filter_var_dict(frame.f_locals)
    f_name = frame.f_code.co_name
    if hasattr(frame, 'f_valuestack'):
        if not is_python3:
            for i, e in enumerate([e for e in frame.f_valuestack if type(e) is list]):
                ret['_tmp' + str(i + 1)] = e

        if f_name.endswith('comp>'):
            for i, e in enumerate([e for e in frame.f_valuestack if type(e) in (list, set, dict)]):
                ret['_tmp' + str(i + 1)] = e

    return ret


def filter_var_dict(d):
    ret = {}
    for k, v in d.items():
        if k not in IGNORE_VARS:
            ret[k] = v

    return ret


def visit_all_locally_reachable_function_objs(frame):
    for k, v in get_user_locals(frame).items():
        for e in visit_function_obj(v, set()):
            if e:
                assert type(e) in (types.FunctionType, types.MethodType)
                yield e


def visit_function_obj(v, ids_seen_set):
    v_id = id(v)
    if v_id in ids_seen_set:
        yield
    else:
        ids_seen_set.add(v_id)
        typ = type(v)
        if typ in (types.FunctionType, types.MethodType):
            yield v
        else:
            if typ in (list, tuple, set):
                for child in v:
                    for child_res in visit_function_obj(child, ids_seen_set):
                        yield child_res

            else:
                if typ == dict or pg_encoder.is_class(v) or pg_encoder.is_instance(v):
                    contents_dict = None
                    if typ == dict:
                        contents_dict = v
                    else:
                        if hasattr(v, '__dict__'):
                            contents_dict = v.__dict__
                    if contents_dict:
                        for key_child, val_child in contents_dict.items():
                            for key_child_res in visit_function_obj(key_child, ids_seen_set):
                                yield key_child_res

                            for val_child_res in visit_function_obj(val_child, ids_seen_set):
                                yield val_child_res

        yield


class PGLogger(bdb.Bdb):

    def __init__(self, cumulative_mode, heap_primitives, show_only_outputs, finalizer_func, disable_security_checks=False, crazy_mode=False):
        bdb.Bdb.__init__(self)
        self.mainpyfile = ''
        self._wait_for_mainpyfile = 0
        self.disable_security_checks = disable_security_checks
        self.cumulative_mode = cumulative_mode
        self.render_heap_primitives = heap_primitives
        self.show_only_outputs = show_only_outputs
        self.crazy_mode = crazy_mode
        self.finalizer_func = finalizer_func
        self.trace = []
        self.done = False
        self.wait_for_return_stack = None
        self.GAE_STDOUT = sys.stdout
        self.closures = {}
        self.lambda_closures = {}
        self.globally_defined_funcs = set()
        self.frame_ordered_ids = {}
        self.cur_frame_id = 1
        self.zombie_frames = []
        self.parent_frames_set = set()
        self.all_globals_in_order = []
        self.encoder = pg_encoder.ObjectEncoder(self.render_heap_primitives)
        self.executed_script = None
        self.breakpoints = []
        self.prev_lineno = -1

    def get_frame_id(self, cur_frame):
        return self.frame_ordered_ids[cur_frame]

    def get_parent_of_function(self, val):
        if val in self.closures:
            return self.get_frame_id(self.closures[val])
        if val in self.lambda_closures:
            return self.get_frame_id(self.lambda_closures[val])
        return

    def get_parent_frame(self, frame):
        for func_obj, parent_frame in self.closures.items():
            if func_obj.__code__ == frame.f_code:
                all_matched = True
                for k in frame.f_locals:
                    if k in frame.f_code.co_varnames:
                        continue
                    if k != '__return__' and k in parent_frame.f_locals and parent_frame.f_locals[k] != frame.f_locals[k]:
                        all_matched = False
                        break

                if all_matched:
                    return parent_frame

        for lambda_code_obj, parent_frame in self.lambda_closures.items():
            if lambda_code_obj == frame.f_code:
                return parent_frame

    def lookup_zombie_frame_by_id(self, frame_id):
        for e in self.zombie_frames:
            if self.get_frame_id(e) == frame_id:
                return e

        assert False

    def forget(self):
        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

    def setup(self, f, t):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, t)
        self.curframe = self.stack[self.curindex][0]

    def get_stack_code_IDs(self):
        return [id(e[0].f_code) for e in self.stack]

    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self.done:
            return
        if self._wait_for_mainpyfile:
            return
        if self.stop_here(frame):
            try:
                del frame.f_locals['__return__']
            except KeyError:
                pass

            self.interaction(frame, None, 'call')

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        if self.done:
            return
        if self._wait_for_mainpyfile:
            if self.canonic(frame.f_code.co_filename) != '<string>' or frame.f_lineno <= 0:
                return
            self._wait_for_mainpyfile = 0
        self.interaction(frame, None, 'step_line')

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        if self.done:
            return
        frame.f_locals['__return__'] = return_value
        self.interaction(frame, None, 'return')

    def user_exception(self, frame, exc_info):
        """This function is called if an exception occurs,
        but only if we are to stop at or just below this level."""
        if self.done:
            return
        else:
            exc_type, exc_value, exc_traceback = exc_info
            frame.f_locals['__exception__'] = (exc_type, exc_value)
            if type(exc_type) == type(''):
                exc_type_name = exc_type
            else:
                exc_type_name = exc_type.__name__
            if exc_type_name == 'RawInputException':
                raw_input_arg = str(exc_value.args[0])
                self.trace.append(dict(event='raw_input', prompt=raw_input_arg))
                self.done = True
            else:
                if exc_type_name == 'MouseInputException':
                    mouse_input_arg = str(exc_value.args[0])
                    self.trace.append(dict(event='mouse_input', prompt=mouse_input_arg))
                    self.done = True
                else:
                    self.interaction(frame, exc_traceback, 'exception')

    def get_script_line(self, n):
        return self.executed_script_lines[(n - 1)]

    def interaction(self, frame, traceback, event_type):
        self.setup(frame, traceback)
        tos = self.stack[self.curindex]
        top_frame = tos[0]
        lineno = tos[1]
        if self.canonic(top_frame.f_code.co_filename) != '<string>':
            return
        if top_frame.f_code.co_name == '__new__':
            return
        if top_frame.f_code.co_name == '__repr__':
            return
        if '__OPT_toplevel__' not in top_frame.f_globals:
            return
        if self.wait_for_return_stack:
            if event_type == 'return':
                if self.wait_for_return_stack == self.get_stack_code_IDs():
                    self.wait_for_return_stack = None
            return
        if event_type == 'call':
            func_line = self.get_script_line(top_frame.f_code.co_firstlineno)
            if CLASS_RE.match(func_line.lstrip()):
                self.wait_for_return_stack = self.get_stack_code_IDs()
                return
        self.encoder.reset_heap()
        if event_type == 'call':
            self.frame_ordered_ids[top_frame] = self.cur_frame_id
            self.cur_frame_id += 1
            if self.cumulative_mode:
                self.zombie_frames.append(top_frame)
            cur_stack_frames = [e[0] for e in self.stack[:self.curindex + 1]]
            zombie_frames_to_render = [e for e in self.zombie_frames if e not in cur_stack_frames]
            encoded_stack_locals = []

            def create_encoded_stack_entry(cur_frame):
                ret = {}
                parent_frame_id_list = []
                f = cur_frame
                while True:
                    p = self.get_parent_frame(f)
                    if p:
                        pid = self.get_frame_id(p)
                        assert pid
                        parent_frame_id_list.append(pid)
                        f = p
                    else:
                        break

                cur_name = cur_frame.f_code.co_name
                if cur_name == '':
                    cur_name = 'unnamed function'
                if cur_name == '<lambda>':
                    cur_name += pg_encoder.create_lambda_line_number(cur_frame.f_code, self.encoder.line_to_lambda_code)
                encoded_locals = {}
                for k, v in get_user_locals(cur_frame).items():
                    is_in_parent_frame = False
                    for pid in parent_frame_id_list:
                        parent_frame = self.lookup_zombie_frame_by_id(pid)
                        if k in parent_frame.f_locals and k != '__return__' and parent_frame.f_locals[k] == v:
                            is_in_parent_frame = True

                    if is_in_parent_frame:
                        if k not in cur_frame.f_code.co_varnames:
                            continue
                    if k == '__module__':
                        continue
                    encoded_val = self.encoder.encode(v, self.get_parent_of_function)
                    encoded_locals[k] = encoded_val

                ordered_varnames = []
                for e in cur_frame.f_code.co_varnames:
                    if e in encoded_locals:
                        ordered_varnames.append(e)

                for e in sorted(encoded_locals.keys()):
                    if e != '__return__' and e not in ordered_varnames:
                        ordered_varnames.append(e)

                if '__return__' in encoded_locals:
                    ordered_varnames.append('__return__')
                if '__locals__' in encoded_locals:
                    ordered_varnames.remove('__locals__')
                    local = encoded_locals.pop('__locals__')
                    if encoded_locals.get('__return__', True) is None:
                        encoded_locals['__return__'] = local
                assert len(ordered_varnames) == len(encoded_locals)
                for e in ordered_varnames:
                    assert e in encoded_locals

                return dict(func_name=cur_name,
                  is_parent=(cur_frame in self.parent_frames_set),
                  frame_id=(self.get_frame_id(cur_frame)),
                  parent_frame_id_list=parent_frame_id_list,
                  encoded_locals=encoded_locals,
                  ordered_varnames=ordered_varnames)

            i = self.curindex
            if i > 1:
                for v in visit_all_locally_reachable_function_objs(top_frame):
                    if v not in self.closures and v not in self.globally_defined_funcs:
                        chosen_parent_frame = None
                        for my_frame, my_lineno in reversed(self.stack):
                            if chosen_parent_frame:
                                break
                            for frame_const in my_frame.f_code.co_consts:
                                if frame_const is (v.__code__ if is_python3 else v.func_code):
                                    chosen_parent_frame = my_frame
                                    break

                        if chosen_parent_frame in self.frame_ordered_ids:
                            self.closures[v] = chosen_parent_frame
                            self.parent_frames_set.add(chosen_parent_frame)
                            if chosen_parent_frame not in self.zombie_frames:
                                self.zombie_frames.append(chosen_parent_frame)
                else:
                    if top_frame.f_code.co_consts:
                        for e in top_frame.f_code.co_consts:
                            if type(e) == types.CodeType and e.co_name == '<lambda>':
                                self.lambda_closures[e] = top_frame
                                self.parent_frames_set.add(top_frame)
                                if top_frame not in self.zombie_frames:
                                    self.zombie_frames.append(top_frame)

        else:
            for k, v in get_user_globals(top_frame).items():
                if type(v) in (types.FunctionType, types.MethodType) and v not in self.closures:
                    self.globally_defined_funcs.add(v)

        while True:
            cur_frame = self.stack[i][0]
            cur_name = cur_frame.f_code.co_name
            if cur_name == '<module>':
                break
            if cur_frame in self.frame_ordered_ids:
                encoded_stack_locals.append(create_encoded_stack_entry(cur_frame))
            i -= 1

        zombie_encoded_stack_locals = [create_encoded_stack_entry(e) for e in zombie_frames_to_render]
        encoded_globals = {}
        for k, v in get_user_globals((tos[0]),
          at_global_scope=(self.curindex <= 1)).items():
            encoded_val = self.encoder.encode(v, self.get_parent_of_function)
            encoded_globals[k] = encoded_val
            if k not in self.all_globals_in_order:
                self.all_globals_in_order.append(k)

        ordered_globals = [e for e in self.all_globals_in_order if e in encoded_globals]
        assert len(ordered_globals) == len(encoded_globals)
        stack_to_render = []
        if encoded_stack_locals:
            for e in encoded_stack_locals:
                e['is_zombie'] = False
                e['is_highlighted'] = False
                stack_to_render.append(e)

            stack_to_render[0]['is_highlighted'] = True
        for e in zombie_encoded_stack_locals:
            e['is_zombie'] = True
            e['is_highlighted'] = False
            stack_to_render.append(e)

        stack_to_render.sort(key=(lambda e: e['frame_id']))
        for e in stack_to_render:
            hash_str = e['func_name']
            hash_str += '_f' + str(e['frame_id'])
            if e['is_parent']:
                hash_str += '_p'
            if e['is_zombie']:
                hash_str += '_z'
            e['unique_hash'] = hash_str

        if self.show_only_outputs:
            trace_entry = dict(line=lineno,
              event=event_type,
              func_name=(tos[0].f_code.co_name),
              globals={},
              ordered_globals=[],
              stack_to_render=[],
              heap={},
              stdout=(get_user_stdout(tos[0])))
        else:
            trace_entry = dict(line=lineno,
              event=event_type,
              func_name=(tos[0].f_code.co_name),
              globals=encoded_globals,
              ordered_globals=ordered_globals,
              stack_to_render=stack_to_render,
              heap=(self.encoder.get_heap()),
              stdout=(get_user_stdout(tos[0])))
        if self.crazy_mode:
            trace_entry['column'] = frame.f_colno
            if frame.f_lasti >= 0:
                key = (frame.f_code.co_code,
                 frame.f_lineno,
                 frame.f_colno,
                 frame.f_lasti)
                if key in self.bytecode_map:
                    v = self.bytecode_map[key]
                    trace_entry['expr_start_col'] = v.start_col
                    trace_entry['expr_width'] = v.extent
                    trace_entry['opcode'] = v.opcode
        if __html__:
            trace_entry['html_output'] = __html__
        if __css__:
            trace_entry['css_output'] = __css__
        if __js__:
            trace_entry['js_output'] = __js__
        if event_type == 'exception':
            exc = frame.f_locals['__exception__']
            trace_entry['exception_msg'] = exc[0].__name__ + ': ' + str(exc[1])
        append_to_trace = True
        if self.breakpoints and not lineno in self.breakpoints:
            if not self.prev_lineno in self.breakpoints:
                append_to_trace = False
            if event_type == 'exception':
                append_to_trace = True
            self.prev_lineno = lineno
            if append_to_trace:
                self.trace.append(trace_entry)
            if len(self.trace) >= MAX_EXECUTED_LINES:
                self.trace.append(dict(event='instruction_limit_reached',
                  exception_msg=('Stopped after running ' + str(MAX_EXECUTED_LINES) + ' steps. Please shorten your code,\nsince Python Tutor is not designed to handle long-running code.')))
                self.force_terminate()
        self.forget()

    def _runscript(self, script_str, custom_globals=None):
        self.executed_script = script_str
        self.executed_script_lines = self.executed_script.splitlines()
        for i, line in enumerate(self.executed_script_lines):
            line_no = i + 1
            if line.endswith(BREAKPOINT_STR):
                self.breakpoints.append(line_no)

        if self.crazy_mode:
            import super_dis
            try:
                self.bytecode_map = super_dis.get_bytecode_map(self.executed_script)
            except:
                self.bytecode_map = {}

        else:
            self._wait_for_mainpyfile = 1
            user_builtins = {}
            if type(__builtins__) is dict:
                builtin_items = __builtins__.items()
            else:
                assert type(__builtins__) is types.ModuleType
                builtin_items = []
                for k in dir(__builtins__):
                    builtin_items.append((k, getattr(__builtins__, k)))

        for k, v in builtin_items:
            if k == 'open':
                user_builtins[k] = open_wrapper
            elif k in BANNED_BUILTINS:
                user_builtins[k] = create_banned_builtins_wrapper(k)
            elif k == '__import__':
                user_builtins[k] = __restricted_import__
            elif k == 'raw_input':
                user_builtins[k] = raw_input_wrapper
            elif k == 'input':
                if is_python3:
                    user_builtins[k] = raw_input_wrapper
                else:
                    user_builtins[k] = python2_input_wrapper
            else:
                user_builtins[k] = v

        user_builtins['mouse_input'] = mouse_input_wrapper
        user_builtins['setHTML'] = setHTML
        user_builtins['setCSS'] = setCSS
        user_builtins['setJS'] = setJS
        user_stdout = StringIO.StringIO()
        sys.stdout = user_stdout
        self.ORIGINAL_STDERR = sys.stderr
        user_globals = {'__name__':'__main__', 
         '__builtins__':user_builtins, 
         '__user_stdout__':user_stdout, 
         '__OPT_toplevel__':True}
        if custom_globals:
            user_globals.update(custom_globals)
        try:
            if resource_module_loaded:
                if not self.disable_security_checks:
                    resource.setrlimit(resource.RLIMIT_AS, (200000000, 200000000))
                    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
                    resource.setrlimit(resource.RLIMIT_NOFILE, (0, 0))
                    for a in dir(sys.modules['posix']):
                        delattr(sys.modules['posix'], a)

                    for a in dir(sys.modules['os']):
                        if a not in ('path', 'stat'):
                            delattr(sys.modules['os'], a)

                    import gc
                    for a in dir(sys.modules['gc']):
                        delattr(sys.modules['gc'], a)

                    del sys.modules['gc']
                    del sys.modules['os']
                    del sys.modules['os.path']
                    del sys.modules['sys']
            self.run(script_str, user_globals, user_globals)
        except SystemExit:
            raise bdb.BdbQuit
        except:
            if DEBUG:
                traceback.print_exc()
            else:
                trace_entry = dict(event='uncaught_exception')
                exc_type, exc_val, exc_tb = sys.exc_info()
                if hasattr(exc_val, 'lineno'):
                    trace_entry['line'] = exc_val.lineno
                if hasattr(exc_val, 'offset'):
                    trace_entry['offset'] = exc_val.offset
                trace_entry['exception_msg'] = type(exc_val).__name__ + ': ' + str(exc_val)
                already_caught = False
                for e in self.trace:
                    if e['event'] == 'exception':
                        already_caught = True
                        break

                if not already_caught:
                    if not self.done:
                        self.trace.append(trace_entry)
            raise bdb.BdbQuit

    def force_terminate(self):
        raise bdb.BdbQuit

    def finalize(self):
        sys.stdout = self.GAE_STDOUT
        sys.stderr = self.ORIGINAL_STDERR
        assert len(self.trace) <= MAX_EXECUTED_LINES + 1
        res = self.trace
        if len(res) >= 2:
            if res[(-2)]['event'] == 'exception':
                if res[(-1)]['event'] == 'return':
                    if res[(-1)]['func_name'] == '<module>':
                        res.pop()
        self.trace = res
        return self.finalizer_func(self.executed_script, self.trace)


import json

def exec_script_str(script_str, raw_input_lst_json, options_json, finalizer_func):
    global __css__
    global __html__
    global __js__
    global input_string_queue
    options = json.loads(options_json)
    py_crazy_mode = 'py_crazy_mode' in options and options['py_crazy_mode']
    logger = PGLogger((options['cumulative_mode']),
      (options['heap_primitives']),
      (options['show_only_outputs']),
      finalizer_func,
      crazy_mode=py_crazy_mode)
    input_string_queue = []
    if raw_input_lst_json:
        input_string_queue = [str(e) for e in json.loads(raw_input_lst_json)]
    __html__, __css__, __js__ = (None, None, None)
    try:
        try:
            logger._runscript(script_str)
        except bdb.BdbQuit:
            pass

    finally:
        logger.finalize()


def exec_script_str_local(script_str, raw_input_lst_json, cumulative_mode, heap_primitives, finalizer_func):
    global __css__
    global __html__
    global __js__
    global input_string_queue
    logger = PGLogger(cumulative_mode,
      heap_primitives,
      False,
      finalizer_func,
      disable_security_checks=True)
    input_string_queue = []
    if raw_input_lst_json:
        input_string_queue = [str(e) for e in json.loads(raw_input_lst_json)]
    __html__, __css__, __js__ = (None, None, None)
    try:
        try:
            logger._runscript(script_str)
        except bdb.BdbQuit:
            pass

    finally:
        return

    return logger.finalize()


def exec_str_with_user_ns(script_str, user_ns, finalizer_func):
    global __css__
    global __html__
    global __js__
    logger = PGLogger(False, False, False, finalizer_func, disable_security_checks=True)
    __html__, __css__, __js__ = (None, None, None)
    try:
        try:
            logger._runscript(script_str, user_ns)
        except bdb.BdbQuit:
            pass

    finally:
        return

    return logger.finalize()