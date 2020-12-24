# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\vm\corefuncs.py
# Compiled at: 2014-11-21 21:05:50


def push(i, l, stack):
    topush = int(l[(i + 1)], 16)
    stack.append(topush)


def pop(stack):
    stack.pop()


def clear_s(stack):
    for item in stack:
        stack.remove(item)