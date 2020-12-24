# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/pytutor/pg_logger.py
# Compiled at: 2014-07-18 14:13:27
import sys, bdb, re, traceback, types
is_python3 = sys.version_info[0] == 3
if is_python3:
    import io as cStringIO
else:
    import cStringIO
import pg_encoder
MAX_EXECUTED_LINES = 300
DEBUG = True
try:
    import resource
    resource_module_loaded = True
except ImportError:
    resource_module_loaded = False

if type(__builtins__) is dict:
    BUILTIN_IMPORT = __builtins__['__import__']
else:
    assert type(__builtins__) is types.ModuleType
    BUILTIN_IMPORT = __builtins__.__import__
ALLOWED_MODULE_IMPORTS = (
 'math', 'random', 'datetime',
 'functools', 'operator', 'string',
 'collections', 're', 'json',
 'heapq', 'bisect')
for m in ALLOWED_MODULE_IMPORTS:
    __import__(m)

def __restricted_import__(*args):
    if args[0] in ALLOWED_MODULE_IMPORTS:
        return BUILTIN_IMPORT(*args)
    raise ImportError(('{0} not supported').format(args[0]))


BANNED_BUILTINS = (
 'reload', 'input', 'apply', 'open', 'compile',
 'file', 'eval', 'exec', 'execfile',
 'exit', 'quit', 'raw_input', 'help',
 'dir', 'globals', 'locals', 'vars')
IGNORE_VARS = set(('__user_stdout__', '__builtins__', '__name__', '__exception__', '__doc__', '__package__'))

def get_user_stdout(frame):
    return frame.f_globals['__user_stdout__'].getvalue()


def get_user_globals(frame):
    d = filter_var_dict(frame.f_globals)
    if '__return__' in d:
        del d['__return__']
    return d


def get_user_locals(frame):
    return filter_var_dict(frame.f_locals)


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
        elif typ in (list, tuple, set):
            for child in v:
                for child_res in visit_function_obj(child, ids_seen_set):
                    yield child_res

        elif typ == dict or pg_encoder.is_class(v) or pg_encoder.is_instance(v):
            contents_dict = None
            if typ == dict:
                contents_dict = v
            elif hasattr(v, '__dict__'):
                contents_dict = v.__dict__
            if contents_dict:
                for key_child, val_child in contents_dict.items():
                    for key_child_res in visit_function_obj(key_child, ids_seen_set):
                        yield key_child_res

                    for val_child_res in visit_function_obj(val_child, ids_seen_set):
                        yield val_child_res

        yield
    return


class PGLogger(bdb.Bdb):

    def __init__(self, cumulative_mode, finalizer_func):
        bdb.Bdb.__init__(self)
        self.mainpyfile = ''
        self._wait_for_mainpyfile = 0
        self.finalizer_func = finalizer_func
        self.cumulative_mode = cumulative_mode
        self.trace = []
        self.GAE_STDOUT = sys.stdout
        self.closures = {}
        self.globally_defined_funcs = set()
        self.frame_ordered_ids = {}
        self.cur_frame_id = 1
        self.zombie_frames = []
        self.parent_frames_set = set()
        self.all_globals_in_order = []
        self.encoder = pg_encoder.ObjectEncoder()
        self.executed_script = None
        return

    def get_frame_id(self, cur_frame):
        return self.frame_ordered_ids[cur_frame]

    def get_parent_of_function(self, val):
        if val not in self.closures:
            return None
        else:
            return self.get_frame_id(self.closures[val])

    def get_parent_frame(self, frame):
        for func_obj, parent_frame in self.closures.items():
            if func_obj.__code__ == frame.f_code:
                all_matched = True
                for k in frame.f_locals:
                    if k in frame.f_code.co_varnames:
                        continue
                    if k != '__return__' and k in parent_frame.f_locals:
                        if parent_frame.f_locals[k] != frame.f_locals[k]:
                            all_matched = False
                            break

                if all_matched:
                    return parent_frame

        return

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
        return

    def setup(self, f, t):
        self.forget()
        self.stack, self.curindex = self.get_stack(f, t)
        self.curframe = self.stack[self.curindex][0]

    def user_call(self, frame, argument_list):
        """This method is called when there is the remote possibility
        that we ever need to stop in this function."""
        if self._wait_for_mainpyfile:
            return
        else:
            if self.stop_here(frame):
                try:
                    del frame.f_locals['__return__']
                except KeyError:
                    pass

                self.interaction(frame, None, 'call')
            return

    def user_line(self, frame):
        """This function is called when we stop or break at this line."""
        if self._wait_for_mainpyfile:
            if self.canonic(frame.f_code.co_filename) != '<string>' or frame.f_lineno <= 0:
                return
            self._wait_for_mainpyfile = 0
        self.interaction(frame, None, 'step_line')
        return

    def user_return(self, frame, return_value):
        """This function is called when a return trap is set here."""
        frame.f_locals['__return__'] = return_value
        self.interaction(frame, None, 'return')
        return

    def user_exception(self, frame, exc_info):
        exc_type, exc_value, exc_traceback = exc_info
        frame.f_locals['__exception__'] = (
         exc_type, exc_value)
        if type(exc_type) == type(''):
            exc_type_name = exc_type
        else:
            exc_type_name = exc_type.__name__
        self.interaction(frame, exc_traceback, 'exception')

    def interaction(self, frame, traceback, event_type):
        self.setup(frame, traceback)
        tos = self.stack[self.curindex]
        top_frame = tos[0]
        lineno = tos[1]
        for cur_frame, cur_line in self.stack[1:]:
            if self.canonic(cur_frame.f_code.co_filename) != '<string>':
                return
            if cur_frame.f_code.co_name == '__new__':
                return
            if cur_frame.f_code.co_name == '__repr__':
                return

        self.encoder.reset_heap()
        if event_type == 'call':
            self.frame_ordered_ids[top_frame] = self.cur_frame_id
            self.cur_frame_id += 1
            if self.cumulative_mode:
                self.zombie_frames.append(top_frame)
        cur_stack_frames = [ e[0] for e in self.stack ]
        zombie_frames_to_render = [ e for e in self.zombie_frames if e not in cur_stack_frames ]
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
            encoded_locals = {}
            for k, v in get_user_locals(cur_frame).items():
                is_in_parent_frame = False
                for pid in parent_frame_id_list:
                    parent_frame = self.lookup_zombie_frame_by_id(pid)
                    if k in parent_frame.f_locals:
                        if k != '__return__':
                            if parent_frame.f_locals[k] == v:
                                is_in_parent_frame = True

                if is_in_parent_frame and k not in cur_frame.f_code.co_varnames:
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

            return dict(func_name=cur_name, is_parent=cur_frame in self.parent_frames_set, frame_id=self.get_frame_id(cur_frame), parent_frame_id_list=parent_frame_id_list, encoded_locals=encoded_locals, ordered_varnames=ordered_varnames)

        i = self.curindex
        if i > 1:
            for v in visit_all_locally_reachable_function_objs(top_frame):
                if v not in self.closures and v not in self.globally_defined_funcs:
                    chosen_parent_frame = None
                    for my_frame, my_lineno in self.stack:
                        if chosen_parent_frame:
                            break
                        for frame_const in my_frame.f_code.co_consts:
                            if frame_const is (v.__code__ if is_python3 else v.func_code):
                                chosen_parent_frame = my_frame
                                break

                    assert chosen_parent_frame
                    if chosen_parent_frame in self.frame_ordered_ids:
                        self.closures[v] = chosen_parent_frame
                        self.parent_frames_set.add(chosen_parent_frame)
                        if chosen_parent_frame not in self.zombie_frames:
                            self.zombie_frames.append(chosen_parent_frame)

        else:
            for k, v in get_user_globals(top_frame).items():
                if type(v) in (types.FunctionType, types.MethodType) and v not in self.closures:
                    self.globally_defined_funcs.add(v)

            while True:
                cur_frame = self.stack[i][0]
                cur_name = cur_frame.f_code.co_name
                if cur_name == '<module>':
                    break
                encoded_stack_locals.append(create_encoded_stack_entry(cur_frame))
                i -= 1

            zombie_encoded_stack_locals = [ create_encoded_stack_entry(e) for e in zombie_frames_to_render ]
            encoded_globals = {}
            for k, v in get_user_globals(tos[0]).items():
                encoded_val = self.encoder.encode(v, self.get_parent_of_function)
                encoded_globals[k] = encoded_val
                if k not in self.all_globals_in_order:
                    self.all_globals_in_order.append(k)

            ordered_globals = [ e for e in self.all_globals_in_order if e in encoded_globals ]
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

            stack_to_render.sort(key=lambda e: e['frame_id'])
            for e in stack_to_render:
                hash_str = e['func_name']
                hash_str += '_f' + str(e['frame_id'])
                if e['is_parent']:
                    hash_str += '_p'
                if e['is_zombie']:
                    hash_str += '_z'
                e['unique_hash'] = hash_str

        trace_entry = dict(line=lineno, event=event_type, func_name=tos[0].f_code.co_name, globals=encoded_globals, ordered_globals=ordered_globals, stack_to_render=stack_to_render, heap=self.encoder.get_heap(), stdout=get_user_stdout(tos[0]))
        if event_type == 'exception':
            exc = frame.f_locals['__exception__']
            trace_entry['exception_msg'] = exc[0].__name__ + ': ' + str(exc[1])
        self.trace.append(trace_entry)
        if len(self.trace) >= MAX_EXECUTED_LINES:
            self.trace.append(dict(event='instruction_limit_reached', exception_msg='(stopped after ' + str(MAX_EXECUTED_LINES) + ' steps to prevent possible infinite loop)'))
            self.force_terminate()
        self.forget()
        return

    def _runscript(self, script_str):
        self.executed_script = script_str
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
                if k in BANNED_BUILTINS:
                    continue
                elif k == '__import__':
                    user_builtins[k] = __restricted_import__
                else:
                    user_builtins[k] = v

            user_stdout = cStringIO.StringIO()
            sys.stdout = user_stdout
            user_globals = {'__name__': '__main__', '__builtins__': user_builtins, 
               '__user_stdout__': user_stdout}
            try:
                if resource_module_loaded:
                    resource.setrlimit(resource.RLIMIT_AS, (200000000, 200000000))
                    resource.setrlimit(resource.RLIMIT_CPU, (5, 5))
                    resource.setrlimit(resource.RLIMIT_NOFILE, (0, 0))
                    del sys.modules['os']
                    del sys.modules['sys']
                self.run(script_str, user_globals, user_globals)
            except SystemExit:
                raise bdb.BdbQuit
            except:
                if DEBUG:
                    traceback.print_exc()
                trace_entry = dict(event='uncaught_exception')
                exc_type, exc_val, exc_tb = sys.exc_info()
                if hasattr(exc_val, 'lineno'):
                    trace_entry['line'] = exc_val.lineno
                if hasattr(exc_val, 'offset'):
                    trace_entry['offset'] = exc_val.offset
                trace_entry['exception_msg'] = type(exc_val).__name__ + ': ' + str(exc_val)
                already_caught = False
                for e in self.trace:
                    if e['event'] == 'exception' and e['exception_msg'] == trace_entry['exception_msg']:
                        already_caught = True
                        break

                if not already_caught:
                    self.trace.append(trace_entry)
                raise bdb.BdbQuit

    def force_terminate(self):
        raise bdb.BdbQuit

    def finalize(self):
        sys.stdout = self.GAE_STDOUT
        assert len(self.trace) <= MAX_EXECUTED_LINES + 1
        res = self.trace
        if len(res) >= 2 and res[(-2)]['event'] == 'exception' and res[(-1)]['event'] == 'return' and res[(-1)]['func_name'] == '<module>':
            res.pop()
        self.trace = res
        self.finalizer_func(self.executed_script, self.trace)


def exec_script_str(script_str, cumulative_mode, finalizer_func):
    logger = PGLogger(cumulative_mode, finalizer_func)
    try:
        try:
            logger._runscript(script_str)
        except bdb.BdbQuit:
            pass

    finally:
        logger.finalize()