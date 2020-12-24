# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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