# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/syntax.py
# Compiled at: 2015-03-20 15:36:01
from __future__ import division, unicode_literals
from Queue import Empty
from scheme.symbol import Symbol
from zope.interface import classProvides, implements, implementer, provider
from scheme.macro import Macro, MacroSymbol
from scheme.Globals import Globals
__author__ = b'perkins'

@provider(Macro)
class SyntaxSymbol(Symbol):

    def __init__(self, *args):
        self.line = 0
        if len(args) > 1:
            processer, template = args
            self.setSymbol(template)
            self.setEnv(processer.cenv)

    def __new__(cls, *args):
        template = args[(-1)]
        return super(SyntaxSymbol, cls).__new__(cls, template)

    def setSyntax(self, transformer):
        self.transformer = transformer
        return self

    def setSymbol(self, symbol):
        self.symbol = symbol
        return self

    def setAltEnv(self, env):
        self.altEnv = env
        return self

    def toObject(self, env):
        if not isinstance(self.symbol, Symbol):
            return self.symbol
        else:
            try:
                possibleEnv = Symbol.getEnv(self, env)
            except NameError:
                if hasattr(self, b'altEnv'):
                    try:
                        possibleEnv = Symbol.getEnv(self.symbol, self.altEnv)
                        return Symbol.toObject(self.symbol, self.altEnv)
                    except NameError:
                        possibleEnv = None

                else:
                    possibleEnv = None

            if possibleEnv is not None:
                keys = possibleEnv.keys()
                if self in keys:
                    possibleSymbol = keys[keys.index(self)]
                    if isinstance(possibleSymbol, SyntaxSymbol) and possibleSymbol.transformer == self.transformer:
                        return possibleEnv[self]
            try:
                return self.symbol.toObject(self.env)
            except NameError as e:
                if hasattr(self, b'altEnv'):
                    return self.symbol.toObject(self.altEnv)
                if possibleEnv:
                    import scheme.processer as p
                    return MacroSymbol(self.symbol).setObj(possibleEnv[self])
                raise e

            return

    def getEnv(self, env):
        possibleEnv = None
        try:
            possibleEnv = Symbol.getEnv(self.symbol, env)
        except NameError:
            try:
                possibleEnv = Symbol.getEnv(self.symbol, self.altEnv)
            except NameError:
                pass

        if possibleEnv is not None:
            keys = possibleEnv.keys()
            if self in keys:
                possibleSymbol = keys[keys.index(self)]
                if isinstance(possibleSymbol, SyntaxSymbol) and possibleSymbol.transformer == self.transformer:
                    return possibleEnv
        return self.symbol.getEnv(self.env)

    def setEnv(self, env):
        self.env = env
        return self

    def __repr__(self):
        return b'<SyntaxSymbol %s>' % Symbol.__repr__(self)


@implementer(Macro)
class syntax(object):

    def __init__(self, *args):
        pass

    def __call__(self, processer, template):
        o = SyntaxSymbol(processer, template[0]).setSymbol(template[0])
        return o


Globals[b'syntax'] = syntax()