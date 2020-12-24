# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib64/python2.7/site-packages/scheme/interfaces.py
# Compiled at: 2015-03-20 15:36:01
from zope import interface

class Procedure(interface.Interface):

    def __init__(ast, env):
        """"""
        pass

    def __call__(processer, params):
        """"""
        pass


class Macro(interface.Interface):

    def __init__(ast, env):
        """"""
        pass

    def __call__(processer, params):
        """"""
        pass