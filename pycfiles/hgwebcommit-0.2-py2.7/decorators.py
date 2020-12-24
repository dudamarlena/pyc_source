# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/actions/decorators.py
# Compiled at: 2011-10-28 19:16:45
from hgwebcommit.actions import FunctionAction, manager

def action(name, label, params=None):

    def _wrap(func):
        obj = FunctionAction(name, label, func, params)
        manager.add(obj)
        return func

    return _wrap