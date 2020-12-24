# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\symlinks\repos\boilerplate_dcc_pyside_widget\boilerplate_dcc_pyside_widget\lib\third_party\pysideuic\Compiler\proxy_type.py
# Compiled at: 2015-08-04 11:44:30
from pysideuic.Compiler.misc import Literal, moduleMember

class ProxyType(type):

    def __init__(*args):
        type.__init__(*args)
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