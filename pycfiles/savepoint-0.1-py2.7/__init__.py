# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/savepoint/__init__.py
# Compiled at: 2013-05-24 19:13:20
import sys, inspect, os.path, pickle

class SavePoint(object):

    def __init__(self, path):
        self.path = path

    def __enter__(self):
        caller = inspect.currentframe(1)
        if os.path.exists(self.path):
            with open(self.path) as (fp):
                updated = pickle.load(fp)
            caller.f_globals.update(updated)
            sys.settrace(lambda *args, **keys: None)
            caller.f_trace = self.trace
        self.original_scope = caller.f_globals.copy()

    def trace(self, frame, event, arg):
        raise

    def __exit__(self, type, value, traceback):
        caller = inspect.currentframe(1)
        updated = {}
        for k, v in caller.f_globals.items():
            if k not in self.original_scope or self.original_scope[k] != v:
                updated[k] = v

        if updated:
            with open(self.path, 'w') as (fp):
                pickle.dump(updated, fp)
        return True