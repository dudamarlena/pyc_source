# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/dbc.py
# Compiled at: 2000-03-15 16:55:42
from bytecodehacks.code_editor import Function
from bytecodehacks.ops import *
import dis, new, string
PRECONDITIONS = 1
POSTCONDITIONS = 2
INVARIANTS = 4
EVERYTHING = PRECONDITIONS | POSTCONDITIONS | INVARIANTS
__strength__ = PRECONDITIONS | POSTCONDITIONS

def add_contracts(target_class, contract_class, strength=None):
    if strength is None:
        strength = __strength__
    newmethods = {}
    contractmethods = contract_class.__dict__
    if strength & INVARIANTS:
        inv = contractmethods.get('class_invariants', None)
    for name, meth in target_class.__dict__.items():
        if strength & PRECONDITIONS:
            pre = contractmethods.get('pre_' + name, None)
            if pre is not None:
                meth = add_precondition(meth, pre)
        if strength & POSTCONDITIONS:
            post = contractmethods.get('post_' + name, None)
            if post is not None:
                meth = add_postcondition(meth, post)
        if strength & INVARIANTS and inv and type(meth) is type(add_contracts):
            if name != '__init__':
                meth = add_precondition(meth, inv)
            meth = add_postcondition(meth, inv)
        newmethods[name] = meth

    return new.classobj(target_class.__name__, target_class.__bases__, newmethods)


def add_precondition(meth, cond):
    meth = Function(meth)
    cond = Function(cond)
    mcs = meth.func_code.co_code
    ccs = cond.func_code.co_code
    nlocals = len(meth.func_code.co_varnames)
    nconsts = len(meth.func_code.co_consts)
    nnames = len(meth.func_code.co_names)
    nargs = meth.func_code.co_argcount
    retops = []
    for op in ccs:
        if op.__class__ is RETURN_VALUE:
            newop = JUMP_FORWARD()
            ccs[ccs.index(op)] = newop
            retops.append(newop)
        elif op.op in dis.hasname:
            op.arg = op.arg + nnames
        elif op.op in dis.haslocal:
            if op.arg >= nargs:
                op.arg = op.arg + nlocals
        elif op.op in dis.hasconst:
            op.arg = op.arg + nconsts

    new = POP_TOP()
    mcs.insert(0, new)
    mcs[0:0] = ccs.opcodes
    for op in retops:
        op.label.op = new

    meth.func_code.co_consts.extend(cond.func_code.co_consts)
    meth.func_code.co_varnames.extend(cond.func_code.co_varnames)
    meth.func_code.co_names.extend(cond.func_code.co_names)
    return meth.make_function()


def add_postcondition(meth, cond):
    """ a bit of a monster! """
    meth = Function(meth)
    cond = Function(cond)
    mcode = meth.func_code
    ccode = cond.func_code
    mcs = mcode.co_code
    ccs = ccode.co_code
    nlocals = len(mcode.co_varnames)
    nconsts = len(mcode.co_consts)
    nnames = len(mcode.co_names)
    nargs = ccode.co_argcount
    cretops = []
    Result_index = len(meth.func_code.co_varnames)
    mcode.co_varnames.append('Result')
    old_refs = find_old_refs(cond)
    for op in ccs:
        if op.__class__ is RETURN_VALUE:
            newop = JUMP_FORWARD()
            ccs[ccs.index(op)] = newop
            cretops.append(newop)
        elif op.op in dis.hasname:
            if cond.func_code.co_names[op.arg] == 'Result' and op.__class__ is LOAD_GLOBAL:
                ccs[ccs.index(op)] = LOAD_FAST(Result_index)
            else:
                op.arg = op.arg + nnames
        elif op.op in dis.haslocal:
            if op.arg >= nargs:
                op.arg = op.arg + nlocals + 1
        elif op.op in dis.hasconst:
            op.arg = op.arg + nconsts

    prologue = []
    for ref, load_op in old_refs:
        if ref[0] in mcode.co_varnames:
            prologue.append(LOAD_FAST(mcode.co_varnames.index(ref[0])))
        else:
            prologue.append(LOAD_GLOBAL(mcode.name_index(ref[0])))
        for name in ref[1:]:
            prologue.append(LOAD_ATTR(mcode.name_index(name)))

        lname = string.join(ref, '.')
        lindex = len(mcode.co_varnames)
        mcode.co_varnames.append(lname)
        prologue.append(STORE_FAST(lindex))
        load_op.arg = lindex

    mcs[0:0] = prologue
    mretops = []
    for op in mcs:
        if op.__class__ is RETURN_VALUE:
            newop = JUMP_FORWARD()
            mcs[mcs.index(op)] = newop
            mretops.append(newop)

    n = len(mcs)
    mcs[n:n] = ccs.opcodes
    store_result = STORE_FAST(Result_index)
    mcs.insert(n, store_result)
    for op in mretops:
        op.label.op = store_result

    new = POP_TOP()
    mcs.append(new)
    for op in cretops:
        op.label.op = new

    mcs.append(LOAD_FAST(Result_index))
    mcs.append(RETURN_VALUE())
    mcode.co_consts.extend(ccode.co_consts)
    mcode.co_varnames.extend(ccode.co_varnames)
    mcode.co_names.extend(ccode.co_names)
    return meth.make_function()


def find_old_refs(func):
    chaining = 0
    refs = []
    ref = []
    code = func.func_code
    cs = code.co_code
    i = 0
    while i < len(cs):
        op = cs[i]
        if not chaining:
            if op.__class__ is LOAD_GLOBAL:
                if code.co_names[op.arg] == 'Old':
                    chaining = 1
        elif op.__class__ is LOAD_ATTR:
            ref.append(code.co_names[op.arg])
        else:
            newop = LOAD_FAST(0)
            cs[(i - len(ref) - 1):i] = [newop]
            i = i - len(ref)
            refs.append((ref, newop))
            ref = []
            chaining = 0
        i = i + 1

    return refs


class Uncontracted:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def do(self):
        return self.x / self.y


class Contracts:

    def pre___init__(self, x, y):
        assert y != 0

    def post_do--- This code section failed: ---

 L. 262         0  LOAD_GLOBAL           0  'Old'
                3  LOAD_ATTR             1  'self'
                6  LOAD_ATTR             2  'x'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             2  'x'
               15  COMPARE_OP            2  ==
               18  POP_JUMP_IF_TRUE     27  'to 27'
               21  LOAD_ASSERT              AssertionError
               24  RAISE_VARARGS_1       1  None

 L. 263        27  LOAD_GLOBAL           0  'Old'
               30  LOAD_ATTR             1  'self'
               33  LOAD_ATTR             4  'y'
               36  LOAD_FAST             0  'self'
               39  LOAD_ATTR             4  'y'
               42  COMPARE_OP            2  ==
               45  POP_JUMP_IF_TRUE     54  'to 54'
               48  LOAD_ASSERT              AssertionError
               51  RAISE_VARARGS_1       1  None

 L. 264        54  LOAD_GLOBAL           5  'Result'
               57  LOAD_CONST               0
               60  COMPARE_OP            4  >
               63  POP_JUMP_IF_TRUE     80  'to 80'
               66  LOAD_ASSERT              AssertionError
               69  LOAD_CONST               'Result was %s'
               72  LOAD_GLOBAL           5  'Result'
               75  UNARY_CONVERT    
               76  BINARY_MODULO    
               77  RAISE_VARARGS_2       2  None

Parse error at or near `BINARY_MODULO' instruction at offset 76

    def class_invariants(self):
        assert self.x > 0


Contracted = add_contracts(Uncontracted, Contracts)