# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/quote.py
# Compiled at: 2015-03-20 15:36:01
__author__ = 'perkins'
from zope.interface import implements
from scheme.macro import Macro
from scheme.Globals import Globals
from utils import copy_with_quote

class quote(object):
    implements(Macro)

    def __init__(self):
        pass

    def __call__(self, processer, params):
        if len(params) > 1:
            raise SyntaxError('quote accepts only 1 argument')
        processer.popStack(copy_with_quote(params)[0])
        processer.stackPointer += 1
        return


Globals['quote'] = quote()