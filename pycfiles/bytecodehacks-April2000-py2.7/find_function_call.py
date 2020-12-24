# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/find_function_call.py
# Compiled at: 2000-03-15 15:55:42
from bytecodehacks.code_editor import Function
from bytecodehacks.ops import *

def find_function_call(infunc, calledfuncname, allowkeywords=0, startindex=0):
    i = startindex
    code = infunc.func_code
    cs = code.co_code

    def match(op, name=calledfuncname):
        return getattr(op, 'name', None) == name

    while i < len(cs):
        op = code.co_code[i]
        if match(op):
            try:
                if allowkeywords:
                    return simulate_stack_with_keywords(code, i)
                else:
                    return simulate_stack(code, i)

            except:
                i = i + 1

        i = i + 1

    if allowkeywords:
        return (None, 0)
    else:
        return
        return


def call_stack_length_usage(arg):
    num_keyword_args = arg >> 8
    num_regular_args = arg & 255
    return 2 * num_keyword_args + num_regular_args


def simulate_stack(code, index_start):
    stack = []
    cs = code.co_code
    i, n = index_start, len(cs)
    while i < n:
        op = cs[i]
        if op.__class__ is CALL_FUNCTION and op.arg + 1 == len(stack):
            stack.append(op)
            return stack
        if op.is_jump():
            i = cs.index(op.label.op) + 1
        else:
            op.execute(stack)
            i = i + 1

    raise 'no call found!'


def simulate_stack_with_keywords(code, index_start):
    stack = []
    cs = code.co_code
    i, n = index_start, len(cs)
    while i < n:
        op = cs[i]
        if op.__class__ is CALL_FUNCTION and call_stack_length_usage(op.arg) + 1 == len(stack):
            stack.append(op)
            return (
             stack, op.arg >> 8)
        if op.is_jump():
            i = cs.index(op.label.op) + 1
        else:
            op.execute(stack)
            i = i + 1

    raise 'no call found!'