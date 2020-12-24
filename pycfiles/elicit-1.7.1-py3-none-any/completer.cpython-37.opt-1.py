# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /elicit/completer.py
# Compiled at: 2018-08-13 00:06:39
# Size of source mod 2**32: 2021 bytes
"""
Completer module.
"""
import keyword, builtins

class Completer:

    def __init__(self, namespace):
        assert isinstance(namespace, dict), 'namespace must be a dict type'
        self.namespace = namespace
        self._globals = get_globals()
        self._globals.extend((str(k) for k in namespace.keys()))
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            self.matches = []
            if '.' in text:
                for name, obj in self.namespace.items():
                    for key in dir(obj):
                        if key.startswith('__'):
                            continue
                        lname = '%s.%s' % (name, key)
                        if lname.startswith(text):
                            self.matches.append(lname)

            else:
                for key in self._globals:
                    if key.startswith(text):
                        self.matches.append(key)

        try:
            return self.matches[state]
        except IndexError:
            return


def get_class_members(klass, rv=None):
    if rv is None:
        rv = dir(klass)
    else:
        rv.extend(dir(klass))
    if hasattr(klass, '__bases__'):
        for base in klass.__bases__:
            get_class_members(base, rv)

    return rv


def get_globals():
    rv = keyword.kwlist + dir(builtins)
    return list(set(rv))