# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\vm\math.py
# Compiled at: 2014-11-21 21:10:56


def add(stack):
    topush = stack[(-1)] + stack[(-2)]
    stack.pop()
    stack.pop()
    stack.append(topush)


def subtract(stack):
    topush = stack[(-1)] - stack[(-2)]
    stack.pop()
    stack.pop()
    stack.append(topush)


def divide(stack):
    topush = stack[(-1)] / stack[(-2)]
    stack.pop()
    stack.pop()
    stack.append(topush)


def multiply(stack):
    topush = stack[(-1)] * stack[(-2)]
    stack.pop()
    stack.pop()
    stack.append(topush)