# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gwfhlang/compiler.py
# Compiled at: 2019-03-25 16:05:01
# Size of source mod 2**32: 3372 bytes
from ast import literal_eval
from lark import Transformer
from gwfhlang.parser import get_parser
from arkhe.utils import create_instr
from arkhe.vm import TypeTable
from arkhe.controller import Arkhe
from arkhe.debugger import ADB
from itertools import chain
from textwrap import dedent

def arkhe_int(value):
    dc = value >> 8
    do = value - (dc << 8)
    return (dc, do)


def name(value):
    return list(map(ord, value))


COMP_MAP = {'==':'eq', 
 '!=':'ne', 
 '>':'gt', 
 '<':'lt', 
 '>=':'ge', 
 '<=':'le'}

class Compiler(Transformer):

    def main(self, tokens):
        return list(chain.from_iterable(filter(lambda token: token, tokens)))

    def symset(self, tokens):
        sym, val = tokens
        value = literal_eval(val)
        if val.type == 'INT':
            ops = arkhe_int(value)
        else:
            if val.type == 'STR':
                ops = list(map(ord, value))
                ops.append(TypeTable.STR.value)
            else:
                if val.type == 'BYT':
                    ops = list(map(ord, value.decode('utf8')))
                    ops.append(TypeTable.BYT.value)
        loads = [
         *create_instr(*('load', 0), *name(sym), *(TypeTable.STR.value,)),
         *create_instr(*('load', 1), *ops)]
        return [
         *loads, *create_instr('symset', 0, 1)]

    def comp(self, tokens):
        op1, comp, op2 = tokens
        comp = COMP_MAP.get(comp.children[0].value, 'eq')
        read, regs = self.symread(op1, op2)
        return [*read, *create_instr(comp, *regs)]

    def symread(self, *syms):
        loads = [create_instr('load', n, *name(item), *(TypeTable.STR.value,)) for n, item in enumerate(syms)]
        symreads = [create_instr('symread', n, n) for n in range(len(syms))]
        return (list(chain.from_iterable([*loads, *symreads])), list(range(len(syms))))

    def if_stmt(self, tokens):
        if len(tokens) == 3:
            comp, suite, suite_else = tokens
            loads = [*create_instr(*('load', 29), *arkhe_int(len(suite))),
             *create_instr(*('load', 30), *arkhe_int(len(suite_else))),
             *create_instr(*('load', 31), *arkhe_int(0))]
            code = [
             *loads,
             *comp,
             *create_instr('jfe', 31),
             *create_instr('jfn', 29),
             *suite,
             *create_instr('jfn', 31),
             *create_instr('jfe', 30),
             *suite_else]
        else:
            comp, suite = tokens
            loads = [*create_instr(*('load', 29), *arkhe_int(len(suite))),
             *create_instr(*('load', 30), *arkhe_int(0))]
            code = [
             *loads,
             *comp,
             *create_instr('jfe', 30),
             *create_instr('jfn', 29),
             *suite]
        return code

    def suite(self, tokens):
        return list(chain.from_iterable(tokens))

    def ccall(self, tokens):
        func, *args = tokens
        args, args_regs = (self.symread)(*args)
        return [
         *args, *create_instr(*('load', 27), *name(str(func)), *(TypeTable.STR.value,)), *create_instr(*('ccall', 27), *args_regs, *(28, ))]