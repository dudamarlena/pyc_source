# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\environment.py
# Compiled at: 2016-03-31 02:52:21
# Size of source mod 2**32: 2776 bytes


class Environment:
    __doc__ = '\n    Hold bindings that associate a symbol to an object during the simulation\n    '

    def __init__(self):
        self.bindings = {}

    def define(self, symbol, value):
        self.bindings[symbol] = value

    def define_each(self, symbols, values):
        if len(symbols) != len(values):
            raise ValueError('Inconsistent symbols and values (found symbols %s, values %s)' % (symbols, values))
        for symbol, value in zip(symbols, values):
            self.define(symbol, value)

    def look_up(self, symbol):
        match = self.bindings.get(symbol, None)
        return match

    def dynamic_look_up(self):
        return self.look_up()

    def create_local_environment(self, dynamic_scope=None):
        return LocalEnvironment(self, dynamic_scope)


class LocalEnvironment(Environment):
    __doc__ = '\n    A local environment linked to two other environments, as enclosing lexical scope\n    and previous dynamic scope, respectively.\n    '

    def __init__(self, lexical_scope, dynamic_scope):
        super().__init__()
        assert isinstance(lexical_scope, Environment), 'Environment must be enclosed within other environments (found %s)' % type(lexical_scope)
        self.parent = lexical_scope
        if not not dynamic_scope:
            assert isinstance(dynamic_scope, Environment), 'Environment must be enclosed within other environments (found %s)' % type(dynamic_scope)
        self.dynamic_scope = dynamic_scope

    def look_up(self, symbol):
        result = super().look_up(symbol)
        if result is None:
            result = self.parent.look_up(symbol)
        return result

    def dynamic_look_up(self, symbol):
        result = super().look_up(symbol)
        if result is None:
            if self.dynamic_scope:
                result = self.dynamic_scope.dynamic_look_up(symbol)
        return result