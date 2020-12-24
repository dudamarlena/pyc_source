# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/externals/pysideuic/Compiler/proxy_type.py
# Compiled at: 2020-04-15 12:12:43
# Size of source mod 2**32: 2136 bytes
from pysideuic.Compiler.misc import Literal, moduleMember

class ProxyType(type):

    def __init__(*args):
        (type.__init__)(*args)
        for cls in args[0].__dict__.values():
            if type(cls) is ProxyType:
                cls.module = args[0].__name__

        if not hasattr(args[0], 'module'):
            args[0].module = ''

    def __getattribute__(cls, name):
        try:
            return type.__getattribute__(cls, name)
        except AttributeError:
            if name == 'module':
                raise
            from pysideuic.Compiler.qtproxies import LiteralProxyClass
            return type(name, (LiteralProxyClass,), {'module': moduleMember(type.__getattribute__(cls, 'module'), type.__getattribute__(cls, '__name__'))})

    def __str__(cls):
        return moduleMember(type.__getattribute__(cls, 'module'), type.__getattribute__(cls, '__name__'))

    def __or__(self, r_op):
        return Literal('%s|%s' % (self, r_op))

    def __eq__(self, other):
        return str(self) == str(other)