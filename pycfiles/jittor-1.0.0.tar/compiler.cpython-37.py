# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/compiler.py
# Compiled at: 2020-04-11 06:08:16
# Size of source mod 2**32: 35760 bytes
import subprocess as sp, os, re, sys, inspect, datetime, threading, ctypes
from ctypes import cdll
from ctypes.util import find_library
import jittor_utils as jit_utils
from jittor_utils import LOG, run_cmd, cache_path, find_exe, cc_path, cc_type, cache_path
from . import pyjt_compiler
from . import lock

def find_jittor_path():
    return os.path.dirname(__file__)


def make_cache_dir(cache_path):
    if not os.path.isdir(cache_path):
        LOG.i(f"Create cache dir: {cache_path}")
        os.mkdir(cache_path)


def remove_flags(flags, rm_flags):
    flags = flags.split(' ')
    output = []
    for s in flags:
        for rm in rm_flags:
            if s.startswith(rm):
                break
        else:
            output.append(s)

    return ' '.join(output)


def compile(compiler, flags, inputs, output, combind_build=False):
    global core_link_flags
    global has_cuda

    def do_compile(cmd):
        if jit_utils.cc:
            return jit_utils.cc.cache_compile(cmd, cache_path, jittor_path)
        run_cmd(cmd)
        return True

    link = link_flags
    if output.startswith('jittor_core'):
        link = link + core_link_flags
    output = os.path.join(cache_path, output)
    obj_files = []
    new_inputs = []
    for name in inputs:
        if name.endswith('.o'):
            obj_files.append(name)
        else:
            new_inputs.append(os.path.join(jittor_path, name))
            obj_files.append(os.path.join(cache_path, 'obj_files', os.path.basename(name) + '.o'))

    inputs = new_inputs
    if len(inputs) == 1 or combind_build:
        cmd = f"{compiler} {' '.join(inputs)} {flags} {link} -o {output}"
        return do_compile(cmd)
    oflags = remove_flags(flags, ['-l', '-L', '-Wl,'])
    cmds = []
    for input, obj_file in zip(inputs, obj_files):
        cc = compiler
        nflags = oflags
        if has_cuda:
            if input.endswith('.cu'):
                nflags = convert_nvcc_flags(oflags)
                cc = nvcc_path
        cmd = f"{cc} {input} {nflags} -c {lto_flags} -o {obj_file}"
        cmds.append(cmd)

    jit_utils.run_cmds(cmds, cache_path, jittor_path)
    cmd = f"{compiler} {' '.join(obj_files)} {flags} {lto_flags} {link} -o {output}"
    return do_compile(cmd)


def gen_jit_tests():
    all_src = run_cmd('find -L src/ | grep "cc$"', jittor_path).splitlines()
    jit_declares = []
    re_def = re.compile('JIT_TEST\\((.*?)\\)')
    names = set()
    test_defs = []
    for src_name in all_src:
        src_name = os.path.join(jittor_path, src_name)
        with open(src_name) as (f):
            src = f.read()
        defs = re_def.findall(src)
        for name in defs:
            LOG.vv(f"Find test {name} from {src_name}")
            assert name not in names, f"Conflict test name {name}"
            names.add(name)
            jit_declares.append(f"JIT_TEST({name});")
            test_defs.append(f"\n                /* From {src_name} */\n                // @pyjt({name})\n                static inline void test_{name}() {{ jit_test_{name}(); }} \n            ")

    jit_declares = '\n    '.join(jit_declares)
    jit_src = f"""\n    #pragma once\n    #include "common.h"\n\n    void expect_error(std::function<void()> func) {{\n        try {{ func(); }}\n        catch (...) {{ return; }}\n        CHECK(0) << "Missing error";\n    }}\n\n    namespace jittor {{\n    \n    {jit_declares}\n\n    // @pyjt(tests)\n    // @attrs(submodule)\n    namespace tests {{\n        {''.join(test_defs)}\n    }}\n\n    }} // jittor\n    """
    LOG.vvvv(jit_src)
    with open(os.path.join(cache_path, 'gen', 'jit_tests.h'), 'w') as (f):
        f.write(jit_src)


def gen_jit_flags():
    all_src = run_cmd('find -L src/ | grep "cc$"', jittor_path).splitlines()
    jit_declares = []
    re_def = re.compile('DEFINE_FLAG(_WITH_SETTER)?\\((.*?)\\);', re.DOTALL)
    flags_defs = []
    visit = {}
    for src_name in all_src:
        src_name = os.path.join(jittor_path, src_name)
        with open(src_name) as (f):
            src = f.read()
        defs = re_def.findall(src)
        for _, args in defs:
            args = args.split(',')
            type = args[0].strip()
            name = args[1].strip()
            if not has_cuda:
                if 'cuda' in name:
                    if name != 'use_cuda':
                        continue
            default = args[2].strip()
            doc = ','.join(args[3:])
            doc = eval(f"({doc})")
            LOG.vv(f"Find define {name} from {src_name}")
            if name in visit:
                continue
            visit[name] = 1
            jit_declares.append(f"DECLARE_FLAG({type}, {name});")
            flags_defs.append(f"\n                /* {name}(type:{type}, default:{default}): {doc} */\n                // @pyjt(__get__{name})\n                {type} _get_{name}() {{ return {name}; }}\n                // @pyjt(__set__{name})\n                void _set_{name}({type} v) {{ set_{name}(v); }}\n                {// @pyjt(__set__{name})\n                void _set_{name}(bool v) {{ set_{name}(v); }}\n                 if type == 'int' else ''}\n            ")

    jit_declares = '\n    '.join(jit_declares)
    jit_src = f"""\n    #include "utils/flags.h"\n\n    namespace jittor {{\n    \n    {jit_declares}\n\n    // @pyjt(flags)\n    struct _Flags {{\n        // @pyjt(__init__)\n        _Flags() {{}}\n        {''.join(flags_defs)}\n    }};\n\n    }} // jittor\n    """
    LOG.vvvv(jit_src)
    with open(os.path.join(cache_path, 'gen', 'jit_flags.h'), 'w') as (f):
        f.write(jit_src)


def gen_jit_op_maker(op_headers, export=False, extra_flags=''):

    def add_src(cc_func_name, cc_args, op_name, op_args, src, pybind_name, py_args, jit_cc_src, doc_string, attrs):
        has_ir = set(['add', 'sub', 'mul', 'matmul', 'truediv', 'floordiv', 'mod', 'divmod', 'pow', 'lshift', 'rshift', 'and', 'xor', 'or'])
        pybind_names = [s.strip() for s in pybind_name.split(',')]
        cc_make_args = [arg.replace('VarHolder*', 'Var*') for arg in cc_args]
        op_make_args = [arg.replace('->var', '') for arg in op_args]
        py_args = [arg.replace('Var*', 'VarHolder*') for arg in py_args]
        op_args = []
        cc_args_with_default = []
        for i, arg in enumerate(cc_args):
            pre_arg = arg.split()[(-1)].split('=')[0]
            op_arg = None
            if arg.startswith('VarHolder*'):
                op_arg = pre_arg + '->var'
            else:
                if arg.startswith('vector<VarHolder*>'):
                    op_arg = f"convert({pre_arg})"
            if '&&' in arg:
                if op_arg == None:
                    op_arg = 'move(' + pre_arg + ')'
                op_make_args[i] = 'move(' + pre_arg + ')'
            if op_arg == None:
                op_arg = pre_arg
            op_args.append(op_arg)
            py_arg = py_args[i]
            if '_a=' not in py_arg:
                cc_args_with_default.append(arg)
                continue
            py_arg = py_arg.split('_a=')[1]
            cc_args_with_default.append(arg + '=' + py_arg)

        cc_args = cc_args_with_default
        if 'multiple_outputs' not in attrs:
            jit_cc_src.append(f"""\n            VarPtr make_{cc_func_name}({', '.join(cc_make_args)}) {{\n                Op* _op = new {op_name}({', '.join(op_make_args)});\n                if (_op->outputs_holder.size() != 1) {{\n                    delete _op;\n                    LOGf << "Wrong output size of" << "{op_name}";\n                }}\n                if (_op->flags.get(NodeFlags::_forwarded)) {{\n                    VarPtr output(move(_op->outputs_holder[0]));\n                    delete _op;\n                    return output;\n                }}\n                _op->outputs_holder[0]->set_inputs({{_op}});\n                VarPtr output(move(_op->outputs_holder[0]));\n                {src.replace('->var', '')};\n                _op->init();\n                return output;\n            }}\n            """)
        else:
            jit_cc_src.append(f"\n            vector<VarPtr> make_{cc_func_name}({', '.join(cc_make_args)}) {{\n                Op* _op = new {op_name}({', '.join(op_make_args)});\n                if (_op->flags.get(NodeFlags::_forwarded)) {{\n                    vector<VarPtr> outputs = move(_op->outputs_holder);\n                    delete _op;\n                    return outputs;\n                }}\n                vector<VarPtr> outputs = move(_op->outputs_holder);\n                for (uint i=0; i<outputs.size(); i++)\n                    outputs[i]->set_inputs({{_op}});\n                {src.replace('->var', '')};\n                _op->init();\n                return outputs;\n            }}\n            ")
        if pybind_name == 'None':
            return
        else:
            pyjt_names = []
            for pybind_name in pybind_names:
                if pybind_name.startswith('__'):
                    pyjt_names.append('Var.' + pybind_name)
                else:
                    pyjt_names.append(pybind_name)
                if len(cc_args) > 0 and cc_args[0].startswith('VarHolder* '):
                    pyjt_names.append('Var.' + pybind_name)

            if 'multiple_outputs' in attrs:
                jit_cc_src.append(f"\n            /*{doc_string}*/\n            // @pyjt({','.join(pyjt_names)})\n            vector<VarHolder*> {cc_func_name}({', '.join(cc_args)}) {{\n                return make_vh_vector(make_{cc_func_name}({', '.join(op_args)}));\n            }}\n            ")
            else:
                jit_cc_src.append(f"\n            /*{doc_string}*/\n            // @pyjt({','.join(pyjt_names)})\n            VarHolder* {cc_func_name}({', '.join(cc_args)}) {{\n                return new VarHolder(make_{cc_func_name}({', '.join(op_args)}));\n            }}\n            ")
        need_ir_define = False
        ir_name = None
        for pybind_name in pybind_names:
            if pybind_name.startswith('__'):
                if pybind_name[2:-2] in has_ir:
                    need_ir_define = True
                    if not ir_name is None:
                        raise AssertionError
                ir_name = pybind_name[2:-2]

        if need_ir_define:
            if not (len(cc_args) > 0 and cc_args[0].startswith('VarHolder* ')):
                raise AssertionError
            this = cc_args[0].split()[(-1)]
            jit_cc_src.append(f"\n            // @pyjt(Var.__i{ir_name}__)\n            // @attrs(return_self)\n            VarHolder* i{cc_func_name}({', '.join(cc_args)}) {{\n                *{this} = make_{cc_func_name}({', '.join(op_args)});\n                return {this};\n            }}\n            ")
            if not (len(cc_args) > 1 and cc_args[1].startswith('VarHolder* ')):
                raise AssertionError(cc_args)
            r_cc_args = [
             cc_args[1], cc_args[0]] + cc_args[2:]
            r_py_args = [py_args[1], py_args[0]] + py_args[2:]
            jit_cc_src.append(f"\n            VarHolder* r{cc_func_name}({', '.join(r_cc_args)}) {{\n                return new VarHolder(make_{cc_func_name}({', '.join(op_args)}));\n            }}\n            ")

    jit_cc_src = []
    jit_headers = ''
    initer = []
    pybind_reg = '(/\\*(.*?)\\*/\\s*)?(//\\s*@pybind\\(([^\\n]*)\\)\\s*)?'
    pybind_attrs_reg = pybind_reg + '(//\\s*@attrs\\(([^\\n]*)\\)\\s*)?'
    for header in op_headers:
        name = os.path.basename(header)
        name = os.path.splitext(name)[0]
        assert name.endswith('_op')
        func_name = name[:-3]
        name2 = map(lambda s: s[:1].upper() + s[1:], name.split('_'))
        name2 = ''.join(name2)
        with open((os.path.join(jittor_path, header)), encoding='utf8') as (f):
            src = f.read()
        res = re.findall(pybind_attrs_reg + '(' + name2 + '\\([^\\n]*\\))', src, re.S)
        assert len(res) >= 1, 'Wrong op args in ' + header
        cc_name = os.path.join(jittor_path, header[:-2] + '.cc')
        constructors = []
        for i in range(len(res)):
            name = 'make_' + func_name + '_' * i
            constructors.append(f"{{ &typeid(&{name}), (void*)&{name} }}")

        constructors = ','.join(constructors)
        var_member_reg = '\\n\\s*Var\\b(.*);'
        var_member_match = re.findall(var_member_reg, src)
        var_member_match = ' '.join(var_member_match)
        for c in '*,':
            var_member_match = var_member_match.replace(c, ' ')

        var_member = var_member_match.split()
        LOG.vv('var_member_match ' + var_member_match)
        LOG.vv('var_member ' + str(var_member))
        var_member_src = [f"VAR_MEMBER_NAME_AND_OFFSET({name}, {name2})" for name in var_member]
        var_member_src = ','.join(var_member_src)
        initer.append(f'\n        op_registe({{ "{func_name}", R"({cc_name})", extra_flags, {{{constructors}}}, {{{var_member_src}}} }});')
        for hid, h_def in enumerate(res):
            h_def = list(h_def)
            attrs = {}
            if h_def[4] != '':
                attrs = pyjt_compiler.parse_attrs(h_def[5])
            else:
                del h_def[4:6]
                doc_string = h_def[1].strip()
                h_def = h_def[2:]
                args_def = h_def[2][len(name2) + 1:-1]
                bind_name = h_def[1]
                if bind_name == '':
                    bind_name = func_name
                elif args_def == '':
                    args = []
                else:
                    args = list(map(lambda s: s.split()[(-1)].split('=')[0], args_def.split(',')))
                py_args = []
                new_args_def = []
                new_args = []
                vh2v_src = []
                more_src = []
                for arg, arg_def in zip(args, args_def.split(',')):
                    py_arg = f'"{arg}"_a'
                    if '=' in arg_def:
                        py_arg += '=' + arg_def.split('=')[(-1)]
                        arg_def = arg_def.split('=')[0]
                    py_args.append(py_arg)
                    arg_type = arg_def[:-(len(arg) + 1)].strip()
                    if arg_type == 'Var*':
                        new_args_def.append('VarHolder* ' + arg)
                        vh2v_src.append(arg + '->var')
                        new_args.append(arg + '->var')
                    elif arg_type.startswith('vector<Var*>'):
                        new_args_def.append(arg_type.replace('Var', 'VarHolder') + ' ' + arg)
                        new_args.append(arg)
                        more_src.append(f"_op->add_inputs({arg});")
                    else:
                        new_args_def.append(arg_def)
                        new_args.append(arg)

                vh2v_src = '_op->set_inputs({' + ', '.join(vh2v_src) + '});' + ''.join(more_src)
                LOG.vvvv(f"Find op: {name2} args: {new_args}")
                if header.startswith('src/'):
                    jit_headers += f'#include "{header[4:]}"\n'
                else:
                    jit_headers += f'#include "{header}"\n'
            add_src(func_name + '_' * hid, new_args_def, name2, new_args, vh2v_src, bind_name, py_args, jit_cc_src, doc_string, attrs)
            if func_name in ('binary', 'unary', 'reduce'):
                with open((os.path.join(jittor_path, f"src/ops/{func_name}_op.cc")), encoding='utf-8') as (f):
                    src = f.read()
                src = src.split(f"unordered_set<string> {func_name}_ops = {{")[1].split('};')[0]
                res2 = re.findall(pybind_reg + '"([a-z_A-Z0-9]*)"', src, re.S)
                res2 = [(_[3], _[4]) for _ in res2]
                LOG.vvvv(f"All supported {func_name} ops: {res2}")
                if func_name == 'reduce':
                    args_def = new_args_def[:1] + new_args_def[2:]
                    py_args_s = py_args[:1] + py_args[2:]
                else:
                    args_def = new_args_def[:-1]
                    py_args_s = py_args[:-1]
                if func_name == 'unary':
                    last_tid = res2.index(('', 'float64'))
                for tid, (bind_name, func_name2) in enumerate(res2):
                    if func_name == 'unary':
                        if tid <= last_tid:
                            func_name3 = func_name2 + '_'
                        else:
                            if func_name == 'reduce':
                                func_name4 = func_name2
                                func_name2 = 'reduce_' + func_name2
                                func_name3 = func_name2
                            else:
                                func_name3 = func_name2
                    else:
                        if len(bind_name) == 0:
                            bind_name = func_name2
                        if func_name == 'reduce':
                            args = new_args[:1] + [f"ns_{func_name4}"] + new_args[2:]
                        else:
                            args = new_args[:-1] + [f"ns_{func_name2}"]
                    add_src(func_name3 + '_' * hid, args_def, name2, args, vh2v_src, bind_name, py_args_s, jit_cc_src, doc_string, attrs)

    jit_src = f"""\n    #pragma once\n    #include "pyjt/py_obj_holder.h"\n    #include "var.h"\n    #include "var_holder.h"\n    #include "ops/op_register.h"\n    {jit_headers}\n    \n    namespace jittor {{\n    // fix make_array(py::array) undefine reference\n    #pragma GCC visibility push(default)\n    #define JIT_NAMESPACE {export + '_maker' if export else 'jit_op_maker'}\n    // @pyjt(ops)\n    // @attrs(submodule{',core_name=' + export if export else ''})\n    namespace JIT_NAMESPACE {{\n    {''.join(jit_cc_src)}\n\n    void initer() {{\n        string extra_flags = R"({extra_flags})";\n        {''.join(initer)}\n    }}\n    int caller = (initer(), 0);\n    \n    }} // JIT_NAMESPACE\n    }} // jittor\n    {\n    namespace jittor {{\n    extern void pyjt_def_{export}(PyObject*);\n    }}\n\n    static void init_module(PyModuleDef* mdef, PyObject* m) {{\n        mdef->m_doc = "User defined custom ops";\n        jittor::pyjt_def_{export}(m);\n    }}\n    PYJF_MODULE_INIT({export});\n\n     if export else ''}\n    """
    return jit_src


@lock.lock_scope()
def compile_custom_op(header, source, op_name, warp=True):
    """Compile a single custom op
    header: code of op header, not path
    source: code of op source, not path
    op_name: op_name of this op, it will used for 
        generation of header and source files, if the 
        type name of op is XxxXxxOp, op_name should be
        xxx_xxx
    warp: if true, warp a snippet for header and source
    """
    if warp:
        header = f'\n        #pragma once\n        #include "op.h"\n        #include "var.h"\n        namespace jittor {{\n        {header}\n        }}\n        '
        source = f'\n        #include "{op_name}_op.h"\n        namespace jittor {{\n        {source}\n        }}\n        '
    cops_dir = os.path.join(cache_path, 'custom_ops')
    make_cache_dir(cops_dir)
    hname = os.path.join(cops_dir, op_name + '_op.h')
    ccname = os.path.join(cops_dir, op_name + '_op.cc')
    with open(hname, 'w') as (f):
        f.write(header)
    with open(ccname, 'w') as (f):
        f.write(source)
    m = compile_custom_ops([hname, ccname])
    return getattr(m, op_name)


@lock.lock_scope()
def compile_custom_ops(filenames, extra_flags='', return_module=False, dlopen_flags=os.RTLD_GLOBAL | os.RTLD_NOW | os.RTLD_DEEPBIND):
    """Compile custom ops
    filenames: path of op source files, filenames must be
        pairs of xxx_xxx_op.cc and xxx_xxx_op.h, and the 
        type name of op must be XxxXxxOp.
    extra_flags: extra compile flags
    return_module: return module rather than ops(default: False)
    return: compiled ops
    """
    global cc_flags
    srcs = {}
    headers = {}
    builds = []
    includes = []
    pyjt_includes = []
    for name in filenames:
        name = os.path.realpath(name)
        if name.endswith('.cc') or name.endswith('.cpp') or name.endswith('.cu'):
            builds.append(name)
        if name.endswith('.h'):
            dirname = os.path.dirname(name)
            if dirname.endswith('inc'):
                includes.append(dirname)
            with open(name, 'r') as (f):
                if '@pyjt' in f.read():
                    pyjt_includes.append(name)
        bname = os.path.basename(name)
        bname = os.path.splitext(bname)[0]
        if bname.endswith('_op'):
            bname = bname[:-3]
            if name.endswith('.cc'):
                srcs[bname] = name
            elif name.endswith('.h'):
                includes.append(os.path.dirname(name))
                headers[bname] = name

    assert len(srcs) == len(headers), 'Source and header names not match'
    for name in srcs:
        assert name in headers, f"Header of op {name} not found"

    gen_name = 'gen_ops_' + '_'.join(headers.keys())
    if len(gen_name) > 100:
        gen_name = gen_name[:80] + '___hash' + str(hash(gen_name))
    includes = set(includes)
    includes = ''.join(map(lambda x: f" -I'{x}' ", includes))
    LOG.vvvv(f"Include flags:{includes}")
    op_extra_flags = includes + extra_flags
    gen_src = gen_jit_op_maker((headers.values()), export=gen_name, extra_flags=op_extra_flags)
    make_cache_dir(os.path.join(cache_path, 'custom_ops'))
    gen_src_fname = os.path.join(cache_path, 'custom_ops', gen_name + '.cc')
    gen_head_fname = os.path.join(cache_path, 'custom_ops', gen_name + '.h')
    gen_lib = os.path.join('custom_ops', gen_name + extension_suffix)
    pyjt_compiler.compile_single(gen_head_fname, gen_src_fname, src=gen_src)
    builds.insert(0, gen_src_fname)

    def insert_anchor(gen_src, anchor_str, insert_str):
        return gen_src.replace(anchor_str, anchor_str + insert_str, 1)

    for name in pyjt_includes:
        LOG.i('handle pyjt_include', name)
        bname = name.split('/')[(-1)].split('.')[0]
        gen_src_fname = os.path.join(cache_path, 'custom_ops', gen_name + '_' + bname + '.cc')
        pyjt_compiler.compile_single(name, gen_src_fname)
        builds.insert(1, gen_src_fname)
        gen_src = insert_anchor(gen_src, 'namespace jittor {', f"extern void pyjt_def_{bname}(PyObject* m);")
        gen_src = insert_anchor(gen_src, 'init_module(PyModuleDef* mdef, PyObject* m) {', f"jittor::pyjt_def_{bname}(m);")

    with open(gen_head_fname, 'w') as (f):
        f.write(gen_src)
    LOG.vvv(f"Build custum ops lib:{gen_lib}")
    LOG.vvvv(f"Build sources:{builds}")
    compile(cc_path, extra_flags + cc_flags + opt_flags + includes, builds, gen_lib)
    LOG.vvv(f"Import custum ops lib:{gen_lib}")
    lib_path = os.path.join(cache_path, 'custom_ops')
    if lib_path not in os.sys.path:
        os.sys.path.append(lib_path)
    with lock.unlock_scope():
        with jit_utils.import_scope(dlopen_flags):
            exec(f"import {gen_name}")
    mod = locals()[gen_name]
    if return_module:
        return mod
    return mod.ops


def get_full_path_of_executable(name):
    full_path = os.path.abspath(name)
    while os.path.islink(full_path):
        full_path = os.path.realpath(full_path)

    if os.path.isfile(full_path):
        if os.access(full_path, os.X_OK):
            return full_path
    return get_full_path_of_executable(find_exe(name))


def compile_extern():
    global kernel_opt_flags
    if cc_type != 'clang':
        return
    cache_path_llvm = os.path.join(cache_path, 'llvm')
    jittor_path_llvm = os.path.join(jittor_path, 'extern', 'llvm')
    clang_dir = os.path.dirname(get_full_path_of_executable(cc_path))
    if not (clang_dir.endswith('bin') and 'llvm' in clang_dir):
        raise AssertionError(f"Wrong clang_dir: {clang_dir}")
    llvm_include = os.path.abspath(os.path.join(clang_dir, '..', 'include'))
    assert os.path.isdir(llvm_include), 'LLVM include path not found'
    make_cache_dir(cache_path_llvm)
    files = os.listdir(jittor_path_llvm)
    test_pass_path = os.path.join(cache_path_llvm, 'test_pass.cc')
    with open(test_pass_path, 'w') as (f):
        f.write('int main() {return 0;}')
    try_flags = [
     ' -Wl,-znodelete -D_GLIBCXX_USE_CXX11_ABI=0 ',
     ' -Wl,-znodelete ']
    found_flags_id = -1
    for fname in files:
        for i, flag in enumerate(try_flags):
            if found_flags_id != -1:
                if found_flags_id != i:
                    continue
            so_name = os.path.join(cache_path_llvm, os.path.splitext(fname)[0] + f".{i}.so")
            compile(cc_path, f"{cc_flags} {opt_flags} {flag} -I'{llvm_include}'", [
             os.path.join(jittor_path_llvm, fname)], so_name)
            if found_flags_id == -1:
                try:
                    s = run_cmd(f"{cc_path} {cc_flags} -Xclang -load -Xclang '{so_name}' {test_pass_path}",
                      cache_path_llvm,
                      print_error=False)
                except Exception as e:
                    try:
                        LOG.v(f"Try flag {flag} failed: {e}")
                        continue
                    finally:
                        e = None
                        del e

                found_flags_id = i
            kernel_opt_flags += f" -Xclang -load -Xclang '{so_name}' "
            break
        else:
            LOG.w('Clang is used, but LLVM pass plugin is unable to link.')
            break

    LOG.vv(f"Compile extern llvm passes: {str(files)}")


def check_cuda():
    global cc_flags
    global core_link_flags
    global cuda_dir
    global cuda_home
    global cuda_include
    global cuda_lib
    global has_cuda
    if nvcc_path == '':
        return
    cuda_dir = os.path.dirname(get_full_path_of_executable(nvcc_path))
    cuda_home = os.path.abspath(os.path.join(cuda_dir, '..'))
    if not (cuda_dir.endswith('bin') and 'cuda' in cuda_dir.lower()):
        raise AssertionError(f"Wrong cuda_dir: {cuda_dir}")
    cuda_include = os.path.abspath(os.path.join(cuda_dir, '..', 'include'))
    cuda_lib = os.path.abspath(os.path.join(cuda_dir, '..', 'lib64'))
    cuda_include2 = os.path.join(jittor_path, 'extern', 'cuda', 'inc')
    cc_flags += f" -DHAS_CUDA -I'{cuda_include}' -I'{cuda_include2}' "
    core_link_flags += f" -lcudart -L'{cuda_lib}' "
    ctypes.CDLL(cuda_lib + '/libcudart.so', dlopen_flags)
    has_cuda = 1


def check_cache_compile():
    global jit_utils_core_files
    files = [
     'src/utils/cache_compile.cc',
     'src/utils/log.cc',
     'src/utils/tracer.cc',
     'src/utils/jit_utils.cc']
    jit_utils_core_files = files
    recompile = compile(cc_path, cc_flags + f" {opt_flags} ", files, 'jit_utils_core' + extension_suffix, True)
    if recompile:
        if jit_utils.cc:
            LOG.e('jit_utils updated, please restart jittor.')
            sys.exit(0)
    if not jit_utils.cc:
        with jit_utils.import_scope(import_flags):
            jit_utils.try_import_jit_utils_core()
        assert jit_utils.cc
        compile(cc_path, cc_flags + f" {opt_flags} ", files, 'jit_utils_core' + extension_suffix, True)


def env_or_try_find(name, bname):
    if name in os.environ:
        path = os.environ[name]
        if path != '':
            version = jit_utils.get_version(path)
            LOG.i(f"Found {bname}{version} at {path}")
        return path
    return try_find_exe(bname)


def try_find_exe(*args):
    try:
        return find_exe(*args)
    except:
        LOG.v(f"{args[0]} not found.")
        return ''


def check_pybt(gdb_path, python_path):
    if gdb_path == '' or python_path == '':
        return False
    ret = sp.getoutput(f"{gdb_path} --batch {python_path} -ex 'help py-bt'")
    if 'python frame' in ret:
        LOG.v('py-bt found in gdb.')
        return True
    return False


def check_debug_flags():
    global cc_flags
    global is_debug
    is_debug = 0
    if os.environ.get('debug') == '1':
        is_debug = 1
        cc_flags += ' -g -DNODE_MEMCHECK '


cc_flags = ' ' + os.environ.get('cc_flags', '')
import_flags = os.RTLD_NOW | os.RTLD_GLOBAL | os.RTLD_DEEPBIND
dlopen_flags = os.RTLD_NOW | os.RTLD_GLOBAL | os.RTLD_DEEPBIND
with jit_utils.import_scope(import_flags):
    jit_utils.try_import_jit_utils_core()
jittor_path = find_jittor_path()
check_debug_flags()
sys.path.append(cache_path)
with jit_utils.import_scope(import_flags):
    jit_utils.try_import_jit_utils_core()
python_path = sys.executable
py3_config_path = sys.executable + '-config'
if not os.path.isfile(python_path):
    raise AssertionError
elif not os.path.isfile(py3_config_path):
    py3_config_path = sys.executable + '3-config'
else:
    assert os.path.isfile(py3_config_path)
    nvcc_path = env_or_try_find('nvcc_path', '/usr/local/cuda/bin/nvcc')
    gdb_path = try_find_exe('gdb')
    addr2line_path = try_find_exe('addr2line')
    has_pybt = check_pybt(gdb_path, python_path)
    cc_flags += ' -Wall -Werror -Wno-unknown-pragmas -std=c++14 -fPIC -march=native '
    link_flags = ' -lstdc++ -ldl -shared '
    core_link_flags = ''
    opt_flags = ''
    kernel_opt_flags = os.environ.get('kernel_flags', '') + opt_flags + ' -fopenmp '
    if ' -O' not in cc_flags:
        opt_flags += ' -O2 '
        kernel_opt_flags += ' -Ofast '
    lto_flags = ''
    if os.environ.get('enable_lto') == '1':
        if cc_type == 'icc':
            lto_flags = ' -flto -ipo -ipo-c '
        else:
            if cc_type == 'g++':
                lto_flags = ' -flto -fuse-linker-plugin '
            else:
                lto_flags = ' -flto '
pybind_include = run_cmd(python_path + ' -m pybind11 --includes')
LOG.i(f"pybind_include: {pybind_include}")
extension_suffix = run_cmd(py3_config_path + ' --extension-suffix')
LOG.i(f"extension_suffix: {extension_suffix}")
make_cache_dir(cache_path)
make_cache_dir(os.path.join(cache_path, 'jit'))
make_cache_dir(os.path.join(cache_path, 'obj_files'))
make_cache_dir(os.path.join(cache_path, 'gen'))
cc_flags += pybind_include
cc_flags += f" -I{jittor_path}/src "
check_cache_compile()
LOG.v(f"Get cache_compile: {jit_utils.cc}")
has_cuda = 0
check_cuda()
nvcc_flags = os.environ.get('nvcc_flags', '')
if has_cuda:
    nvcc_flags += cc_flags + link_flags

    def convert_nvcc_flags(nvcc_flags):
        nvcc_flags = nvcc_flags.replace('-Wall', '')
        nvcc_flags = nvcc_flags.replace('-Wno-unknown-pragmas', '')
        nvcc_flags = nvcc_flags.replace('-fopenmp', '')
        nvcc_flags = nvcc_flags.replace('-march', '-Xcompiler -march')
        nvcc_flags = nvcc_flags.replace('-Werror', '')
        nvcc_flags = nvcc_flags.replace('-fPIC', '-Xcompiler -fPIC')
        nvcc_flags += f" -x cu --cudart=shared -ccbin='{cc_path}' --use_fast_math "
        nvcc_flags += ' -w '
        nvcc_flags += f" -I'{os.path.join(jittor_path, 'extern/cuda/inc')}' "
        if os.environ.get('cuda_debug', '0') == '1':
            nvcc_flags += ' -G '
        return nvcc_flags


    nvcc_flags = convert_nvcc_flags(nvcc_flags)
gen_jit_flags()
gen_jit_tests()
op_headers = run_cmd('find -L src/ops/ | grep "op.h$"', jittor_path).splitlines()
jit_src = gen_jit_op_maker(op_headers)
LOG.vvvv(jit_src)
with open(os.path.join(cache_path, 'gen', 'jit_op_maker.h'), 'w') as (f):
    f.write(jit_src)
cc_flags += f" -I{cache_path} "
pyjt_compiler.compile(cache_path, jittor_path)
files2 = run_cmd(f"""find "{os.path.join(cache_path, 'gen')}" | grep "cc$"""").splitlines()
files4 = run_cmd('find -L src | grep "cc$"', jittor_path).splitlines()
at_beginning = [
 'src/ops/op_utils.cc',
 'src/event_queue.cc',
 'src/mem/allocator/sfrl_allocator.cc',
 'src/mem/allocator.cc']
at_last = [
 'src/profiler/profiler.cc',
 'src/executor.cc',
 'src/fetcher.cc']
for i in range(len(at_beginning)):
    if at_beginning[i] not in files4:
        continue
    files4.remove(at_beginning[i])
    files4.insert(i, at_beginning[i])

for v in at_last:
    if v not in files4:
        continue
    files4.remove(v)
    files4.append(v)

registers = [name for name in files4 if 'register' in name]
for name in registers:
    files4.remove(name)

files = registers + files2 + files4
for file in jit_utils_core_files:
    files.remove(file)

LOG.vv('compile order:', files)
libname = {'clang':'omp', 
 'icc':'iomp5',  'g++':'gomp'}[cc_type]
libname = ctypes.util.find_library(libname)
assert libname is not None, 'openmp library not found'
ctypes.CDLL(libname, os.RTLD_NOW | os.RTLD_GLOBAL)
version_file = os.path.join(jittor_path, 'version')
if os.path.isfile(version_file):
    with open(version_file, 'r') as (f):
        version = f.read().strip()
    key = f"{version}-{cc_type}-{'cuda' if has_cuda else 'cpu'}.o"
    extra_obj = os.path.join(cache_path, key)
    url = os.path.join('https://cg.cs.tsinghua.edu.cn/jittor/assets/build/' + key)
    jit_utils.download(url, extra_obj)
    files.append(extra_obj)
compile(cc_path, cc_flags + opt_flags, files, 'jittor_core' + extension_suffix)
compile_extern()
with jit_utils.import_scope(import_flags):
    import jittor_core as core
flags = core.flags()
if has_cuda:
    nvcc_flags += f" -arch={','.join(map((lambda x: 'sm_' + str(x)), (flags.cuda_archs)))} "
flags.cc_path = cc_path
flags.cc_type = cc_type
flags.cc_flags = cc_flags + link_flags + kernel_opt_flags
flags.nvcc_path = nvcc_path
flags.nvcc_flags = nvcc_flags
flags.python_path = python_path
flags.cache_path = cache_path
flags.jittor_path = jittor_path
flags.gdb_path = gdb_path
flags.addr2line_path = addr2line_path
flags.has_pybt = has_pybt
core.set_lock_path(lock.lock_path)