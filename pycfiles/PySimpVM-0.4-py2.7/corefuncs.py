# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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