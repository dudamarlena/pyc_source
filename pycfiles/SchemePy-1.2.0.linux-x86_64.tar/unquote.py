# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/unquote.py
# Compiled at: 2015-03-20 15:36:01
__author__ = 'perkins'
from scheme.Globals import Globals
from scheme.begin import begin

class unquote(begin):
    pass


class unsyntax(begin):
    pass


Globals['unquote'] = unquote()
Globals['unsyntax'] = unsyntax()