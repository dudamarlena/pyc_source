# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/syntax_rules.py
# Compiled at: 2015-09-04 17:30:49
from __future__ import unicode_literals
from zope.interface import implements, classProvides
from scheme.macro import Macro
from scheme.symbol import Symbol
from scheme.environment import Environment, SyntaxEnvironment
from scheme.syntax import SyntaxSymbol
from scheme.PatternMatcher import PatternMatcher
from scheme.utils import transformCode
import scheme.debug

class syntax_rules(object):
    implements(Macro)
    classProvides(Macro)

    def __init__(self, processer, ast):
        literals = ast[0]
        patterns = ast[1:]
        self.name = patterns[0][0][0]
        self.env = processer.cenv.parent
        self.literals = literals
        self.patterns = patterns

    def __call__(self, processer, params):
        params = params[0].toObject(processer.cenv)
        for pattern in self.patterns:
            template = pattern[1:]
            pattern = pattern[0]
            bindings = PatternMatcher(pattern, self.literals).match(params)
            if bindings is None:
                continue
            env = Environment(self.env)
            l = {}
            l.update(globals())
            l.update(locals())
            transformedCode = transformCode(template, bindings, env, self)
            if scheme.debug.getDebug(b'syntax'):
                print 56, transformedCode
            if len(transformedCode) == 1:
                return transformedCode[0]
            return transformedCode

        raise SyntaxError(b'syntax-rules no case matching %r for %s' % (params, self.name))
        return


import scheme.Globals
scheme.Globals.Globals[b'syntax-rules'] = syntax_rules