# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/let_aster.py
# Compiled at: 2015-03-20 15:36:01
__author__ = 'perkins'
from scheme.macro import Macro
from scheme.Globals import Globals
from zope.interface import implements

class let_aster(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, processer, params):
        env = processer.cenv
        bindings = params[0]
        for binding in bindings:
            if len(binding[1:]) != 1:
                raise SyntaxError('let requires a list of pairs for its first argument')
            env[binding[0]] = processer.process([binding[1]], env)

        processer.process(params[1:], env)


Globals['let*'] = let_aster()