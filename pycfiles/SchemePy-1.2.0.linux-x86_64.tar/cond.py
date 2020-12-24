# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/cond.py
# Compiled at: 2015-03-20 15:36:01
__author__ = 'jeanie'
from scheme.macro import Macro
from scheme.Globals import Globals
from zope.interface import implements

class cond(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, processer, params):
        env = processer.cenv
        for pair in params:
            if pair[0] == 'else':
                return pair[1]
            if isinstance(pair[0], list):
                if processer.process([pair[0]], env):
                    return pair[1]
                continue
            elif pair[0].toObject(env):
                return pair[1]


Globals['cond'] = cond()