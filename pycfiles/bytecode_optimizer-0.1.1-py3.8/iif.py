# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/bytecodehacks/iif.py
# Compiled at: 2000-03-15 16:55:42
from bytecodehacks.code_editor import Function
from bytecodehacks.ops import *
from bytecodehacks.find_function_call import find_function_call

def iifize(func):
    func = Function(func)
    cs = func.func_code.co_code
    while 1:
        stack = find_function_call(func, 'iif')
        if stack is None:
            break
        load, test, consequent, alternative, call = stack
        cs.remove(load)
        jump1 = JUMP_IF_FALSE(alternative)
        cs.insert(cs.index(test) + 1, jump1)
        jump2 = JUMP_FORWARD(call)
        cs.insert(cs.index(consequent) + 1, jump2)
        cs.remove(call)

    cs = None
    return func.make_function()