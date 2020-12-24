# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/syntax_case.py
# Compiled at: 2015-03-20 15:36:01
from __future__ import unicode_literals
from Queue import Empty
from zope.interface import implements, classProvides
from scheme.procedure import Procedure
from scheme.macro import Macro
from scheme.symbol import Symbol
from scheme.environment import Environment, SyntaxEnvironment
from scheme.syntax import SyntaxSymbol
from scheme.PatternMatcher import PatternMatcher
from scheme.utils import transformCode

class syntax_case(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, processer, params):
        e = processer.cenv
        syntax_object = params[0]
        syntax_object = processer.process([syntax_object], e)
        syntax_list = syntax_object.toObject(e)
        while isinstance(syntax_list, SyntaxSymbol):
            syntax_list = syntax_list.toObject(e)

        literals = params[1]
        patterns = params[2:]
        for pattern in patterns:
            if len(pattern) == 2:
                template = pattern[1:]
                pattern = pattern[0]
                guard = True
            else:
                template = pattern[2:]
                guard = pattern[1]
                pattern = pattern[0]
            bindings = PatternMatcher(pattern, literals).match(syntax_list)
            if bindings is None:
                continue
            processer.pushStack([guard])
            icd = processer.callDepth
            r = processer.process([guard], processer.cenv)
            while processer.callDepth > icd:
                processer.popStackN()

            processer.popStack(r)
            if not r:
                continue
            env = Environment(processer.cenv)
            transformedCode = transformCode(template, bindings, env, bindings)
            return transformedCode[0]

        raise SyntaxError(b'syntax-case no case matching %r' % syntax_list)
        return


import scheme.Globals
scheme.Globals.Globals[b'syntax-case'] = syntax_case()
O = []