# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/tailspin/ctailspin.py
# Compiled at: 2009-03-02 23:27:58
from .ctailspin_h import helper

def ctailspin(func):
    func.recur = False

    def help(*args, **kw):
        return helper(func, args, kw)

    return help