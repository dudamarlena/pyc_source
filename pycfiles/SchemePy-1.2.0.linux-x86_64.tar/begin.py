# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/begin.py
# Compiled at: 2015-03-20 15:36:01
__author__ = 'lperkins2'
from zope.interface import implements
from scheme.Globals import Globals
from scheme.macro import Macro

class begin(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, processer, params):
        env = processer.cenv.parent
        retval = None
        for idx, param in enumerate(params):
            processer.stackPointer += 1
            icd = processer.callDepth
            processer.pushStack([param])
            retval = processer.process([param], env, processer.callDepth)
            processer.popStack(retval)
            params[idx] = retval

        processer.popStack(retval)
        processer.stackPointer += 1
        return


Globals['begin'] = begin()