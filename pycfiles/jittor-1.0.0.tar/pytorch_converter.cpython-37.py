# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/utils/pytorch_converter.py
# Compiled at: 2020-04-10 01:50:22
# Size of source mod 2**32: 10489 bytes
import sys, contextlib, os, signal, jittor as jt
jt.dirty_fix_pytorch_runtime_error()
import torch

class CallTree:

    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.children = []
        self.input = []
        self.output = []
        self.args = None
        if parent is not None:
            parent.children.append(self)

    def __str__(self):
        ss = []

        def dfs(v, depth):
            s = '    ' * depth + f"{v.name} in:{v.input} out:{v.output}"
            if v.args is not None:
                s += f" args:{v.args}"
            ss.append(s)
            if len(v.children):
                for c in v.children:
                    dfs(c, depth + 1)

                ss.append(s + ' end')

        dfs(self, 0)
        return '\n'.join(ss)

    def to_jt(self):
        defs = []
        template = {'add':'{0} + {1}', 
         'mul':'{0} * {1}', 
         'getitem':'{0}[{1}]', 
         'gt':'{0} > {1}'}

        def dfs(v):
            if len(v.children) == 0:
                return
            code = []
            code.append(f"def {v.name.split('.')[0]}({','.join(map(str, v.input))}):")
            for c in v.children:
                if c.name == 'BatchNorm2d.forward':
                    bn = c.args['self']
                    code.append(f"    {c.output[0]} = jt.nn.batch_norm({c.input[0]}, is_train={bn.training}, eps={bn.eps}, momentum={bn.momentum})")
                    continue
                if c.name == 'ReLU.forward':
                    code.append(f"    {c.output[0]} = jt.nn.relu({c.input[0]})")
                    continue
                if c.name == 'MaxPool2d.forward':
                    po = c.args['self']
                    code.append(f"    {c.output[0]} = jt.nn.pool({c.input[0]}, size={po.kernel_size}, op='maximum', padding={po.padding}, stride={po.stride})")
                    continue
                if c.name == 'Conv2d.forward':
                    mod = c.args['self']
                    code.append(f"    # {mod}")
                    assert mod.kernel_size[0] == mod.kernel_size[1]
                    assert mod.padding[0] == mod.padding[1]
                    assert mod.stride[0] == mod.stride[1]
                    assert mod.bias == False
                    code.append(f"    {c.output[0]} = nn.conv({c.output[0]}, {mod.in_channels}, {mod.out_channels}, {mod.kernel_size[0]}, {mod.padding[0]}, {mod.stride[0]})")
                    continue
                if c.name.startswith('inj'):
                    if c.name.endswith('__init__'):
                        code.append(f"    {c.args[0]} = jt.array({c.args[1]})")
                    else:
                        if c.name.startswith('inj_torch_Tensor___'):
                            raise c.name.endswith('__') or AssertionError
                        else:
                            name = c.name[19:-2]
                            if name in template:
                                code.append(f"    {c.output[0]} = {(template[name].format)(*c.args)}")
                            else:
                                code.append(f"    {c.output[0]} = __{name}__({', '.join(map(str, c.args))})")
                else:
                    dfs(c)
                    out = ''
                    if len(c.output):
                        out = f"{','.join(map(str, c.output))} = "
                    code.append(f"    {out}{c.name.split('.')[0]}({','.join(map(str, c.input))})")

            if len(v.output):
                code.append(f"    return {','.join(map(str, v.output))}")
            defs.extend(code)

        dfs(self)
        return '\n'.join(defs)


class TNode:

    def __init__(self, s, v):
        self.s = s
        self.v = v

    def __str__(self):
        return self.s

    def __repr__(self):
        return self.s


trace_depth = 0
stack = []
g_vars = {}
g_var_id = 0
g_func_names = []
call_tree = CallTree(None, 'root')

def push_stack(name=None, input=[]):
    global call_tree
    global trace_depth
    trace_depth += 1
    if name is not None:
        if len(stack):
            if stack[(-1)][1].startswith('functional.') or stack[(-1)][1].startswith('inj_'):
                return
        call_tree = CallTree(call_tree, name)
        call_tree.input = input
        stack.append((trace_depth, name))
        return call_tree


def pop_stack(output=[]):
    global call_tree
    global trace_depth
    if len(stack):
        if stack[(-1)][0] == trace_depth:
            stack.pop()
            call_tree.output = output
            call_tree = call_tree.parent
    trace_depth -= 1


def trace_calls(frame, event, arg):
    global g_func_names

    def dfs--- This code section failed: ---

 L. 140         0  LOAD_GLOBAL              isinstance
                2  LOAD_FAST                'obj'
                4  LOAD_GLOBAL              list
                6  CALL_FUNCTION_2       2  '2 positional arguments'
                8  POP_JUMP_IF_FALSE    72  'to 72'

 L. 141        10  SETUP_LOOP          190  'to 190'
               12  LOAD_GLOBAL              enumerate
               14  LOAD_FAST                'obj'
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  GET_ITER         
             20_0  COME_FROM            48  '48'
               20  FOR_ITER             68  'to 68'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'i'
               26  STORE_FAST               'v'

 L. 142        28  LOAD_DEREF               'dfs'
               30  LOAD_FAST                'v'
               32  LOAD_FAST                'func'
               34  CALL_FUNCTION_2       2  '2 positional arguments'
               36  POP_TOP          

 L. 143        38  LOAD_GLOBAL              isinstance
               40  LOAD_FAST                'v'
               42  LOAD_GLOBAL              torch
               44  LOAD_ATTR                Tensor
               46  CALL_FUNCTION_2       2  '2 positional arguments'
               48  POP_JUMP_IF_FALSE    20  'to 20'

 L. 144        50  LOAD_GLOBAL              g_vars
               52  LOAD_GLOBAL              id
               54  LOAD_FAST                'v'
               56  CALL_FUNCTION_1       1  '1 positional argument'
               58  BINARY_SUBSCR    
               60  LOAD_FAST                'obj'
               62  LOAD_FAST                'i'
               64  STORE_SUBSCR     
               66  JUMP_BACK            20  'to 20'
               68  POP_BLOCK        
               70  JUMP_FORWARD        190  'to 190'
             72_0  COME_FROM             8  '8'

 L. 145        72  LOAD_GLOBAL              isinstance
               74  LOAD_FAST                'obj'
               76  LOAD_GLOBAL              dict
               78  CALL_FUNCTION_2       2  '2 positional arguments'
               80  POP_JUMP_IF_FALSE   170  'to 170'

 L. 146        82  SETUP_LOOP          190  'to 190'
               84  LOAD_FAST                'obj'
               86  LOAD_METHOD              items
               88  CALL_METHOD_0         0  '0 positional arguments'
               90  GET_ITER         
             92_0  COME_FROM           146  '146'
               92  FOR_ITER            166  'to 166'
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'k'
               98  STORE_FAST               'v'

 L. 147       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'v'
              104  LOAD_GLOBAL              tuple
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_JUMP_IF_FALSE   126  'to 126'

 L. 148       110  LOAD_GLOBAL              list
              112  LOAD_FAST                'v'
              114  CALL_FUNCTION_1       1  '1 positional argument'
              116  STORE_FAST               'v'

 L. 149       118  LOAD_FAST                'v'
              120  LOAD_FAST                'obj'
              122  LOAD_FAST                'k'
              124  STORE_SUBSCR     
            126_0  COME_FROM           108  '108'

 L. 150       126  LOAD_DEREF               'dfs'
              128  LOAD_FAST                'v'
              130  LOAD_FAST                'func'
              132  CALL_FUNCTION_2       2  '2 positional arguments'
              134  POP_TOP          

 L. 151       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'v'
              140  LOAD_GLOBAL              torch
              142  LOAD_ATTR                Tensor
              144  CALL_FUNCTION_2       2  '2 positional arguments'
              146  POP_JUMP_IF_FALSE    92  'to 92'

 L. 152       148  LOAD_GLOBAL              g_vars
              150  LOAD_GLOBAL              id
              152  LOAD_FAST                'v'
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  BINARY_SUBSCR    
              158  LOAD_FAST                'obj'
              160  LOAD_FAST                'k'
              162  STORE_SUBSCR     
              164  JUMP_BACK            92  'to 92'
              166  POP_BLOCK        
              168  JUMP_FORWARD        190  'to 190'
            170_0  COME_FROM            80  '80'

 L. 153       170  LOAD_GLOBAL              isinstance
              172  LOAD_FAST                'obj'
              174  LOAD_GLOBAL              torch
              176  LOAD_ATTR                Tensor
              178  CALL_FUNCTION_2       2  '2 positional arguments'
              180  POP_JUMP_IF_FALSE   190  'to 190'

 L. 154       182  LOAD_FAST                'func'
              184  LOAD_FAST                'obj'
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  POP_TOP          
            190_0  COME_FROM           180  '180'
            190_1  COME_FROM           168  '168'
            190_2  COME_FROM_LOOP       82  '82'
            190_3  COME_FROM            70  '70'
            190_4  COME_FROM_LOOP       10  '10'

Parse error at or near `COME_FROM_LOOP' instruction at offset 190_2

    if event.endswith('call'):
        co = frame.f_code
        func_name = co.co_name
        func_line_no = frame.f_lineno
        func_filename = co.co_filename
        args = '???'
        t_values = []
        if event == 'c_call':
            func_name = arg.__name__
        else:
            args = list(frame.f_locals.keys())
            if 'self' in frame.f_locals:
                func_name = type(frame.f_locals['self']).__name__ + '.' + func_name
            val = {k:frame.f_locals[k] for k in args}

            def func(v):
                global g_var_id
                if id(v) not in g_vars:
                    if func_name.endswith('__init__'):
                        g_vars[id(v)] = TNode('array_' + str(g_var_id), v)
                    else:
                        g_vars[id(v)] = TNode('input_' + str(g_var_id), v)
                    g_var_id += 1
                t_values.append(g_vars[id(v)])

            dfs(val, func)
        if func_name.endswith('.forward'):
            ct = push_stack(func_name, t_values)
            ct.args = val
        else:
            if func_filename.endswith('functional.py'):
                push_stack('functional.' + func_name, t_values)
            else:
                if func_name.startswith('inj_'):
                    ct = push_stack(func_name, t_values)
                    ct.args = val['a']
                else:
                    if func_name in g_func_names:
                        push_stack(func_name, t_values)
                    else:
                        push_stack()
        jt.LOG.vvvv('----' * trace_depth + f"call: {func_name}({args}){t_values}     # {func_filename}:{func_line_no}")
    else:
        if event.endswith('return'):
            ret = []
            if event == 'c_return':
                jt.LOG.vvvv('----' * trace_depth + f"return {arg.__name__}: ???")
            else:
                co = frame.f_code
                func_name = co.co_name

                def func(arg):
                    global g_var_id
                    if id(arg) not in g_vars:
                        node = TNode(f"out_{g_var_id}", arg)
                        g_vars[id(arg)] = node
                    else:
                        node = g_vars[id(arg)]
                    ret.append(node)
                    g_var_id += 1

                dfs(arg, func)
                if 'self' in frame.f_locals:
                    func_name = type(frame.f_locals['self']).__name__ + '.' + func_name
                jt.LOG.vvvv('----' * trace_depth + f"return {func_name}: {ret}")
            pop_stack(ret)
        return trace_calls


@contextlib.contextmanager
def trace_scope(func_names=[]):
    global g_func_names
    global g_var_id
    global trace_depth
    g_func_names = func_names
    with func_injection():
        try:
            sys.settrace(trace_calls)
            trace_depth = 1
            stack.clear()
            g_vars.clear()
            call_tree.children.clear()
            g_var_id = 0
            yield
        finally:
            sys.settrace(None)
            jt.LOG.v('====================')
            jt.LOG.v(call_tree)


@contextlib.contextmanager
def func_injection():
    global inject_prevs
    names = [
     'torch.Tensor.__init__',
     'torch.Tensor.__add__',
     'torch.Tensor.__mul__',
     'torch.Tensor.__sub__',
     'torch.Tensor.__truediv__',
     'torch.Tensor.__floordiv__',
     'torch.Tensor.__getitem__',
     'torch.Tensor.__pow__',
     'torch.Tensor.__mod__',
     'torch.Tensor.__lt__',
     'torch.Tensor.__le__',
     'torch.Tensor.__gt__',
     'torch.Tensor.__ge__',
     'torch.Tensor.__eq__',
     'torch.Tensor.__ne__',
     'torch.Tensor.__lshift__',
     'torch.Tensor.__rshift__',
     'torch.Tensor.__and__',
     'torch.Tensor.__or__',
     'torch.Tensor.__xor__',
     'torch.Tensor.__abs__',
     'torch.Tensor.__neg__']
    try:
        inject_prevs = []
        for name in names:
            inject_prevs.append(eval(name))

        for i, name in enumerate(names):
            new_name = 'inj_' + name.replace('.', '_')
            if name.endswith('__getitem__'):
                exec(f"def {new_name}(*a): return torch._C._TensorBase.__getitem__(a[0], a[1] if isinstance(a[1], tuple) else (a[1],))")
            else:
                if name.endswith('__init__'):
                    exec(f"def {new_name}(*a, **b): return None")
                else:
                    exec(f"def {new_name}(*a, **b): return inject_prevs[{i}](*a, **b)")
            jt.LOG.v('inject', new_name)
            exec(f"{name} = {new_name}")

        yield
    finally:
        for i, name in enumerate(names):
            prev = inject_prevs[i]
            exec(f"{name} = prev")

        torch.Tensor.__getitem__ = lambda s, a: torch._C._TensorBase.__getitem__(s, a if isinstance(a, tuple) else (a,))