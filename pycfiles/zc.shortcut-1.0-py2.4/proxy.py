# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/proxy.py
# Compiled at: 2006-12-07 13:02:03
"""proxy code for shortcut package

$Id: proxy.py 1585 2005-05-09 15:06:51Z gary $
"""
from zope import interface, proxy
from zope.interface import declarations
try:
    from zope.security.decorator import DecoratedSecurityCheckerDescriptor
except ImportError:
    from zope.decorator import DecoratedSecurityCheckerDescriptor

from zc.shortcut import interfaces

class DecoratorSpecificationDescriptor(declarations.ObjectSpecificationDescriptor):
    """interface declarations on decorators that wish to have their interfaces
    be the most specific, rather than the least (as in 
    DecoratorSpecificationDescriptor)."""
    __module__ = __name__

    def __get__(self, inst, cls=None):
        if inst is None:
            return declarations.getObjectSpecification(cls)
        else:
            provided = interface.providedBy(proxy.getProxiedObject(inst))
            dec_impl = interface.implementedBy(type(inst))
            return declarations.Declaration(dec_impl, provided)
        return

    def __set__(self, inst, v):
        raise TypeError('assignment not allowed')


class Decorator(proxy.ProxyBase):
    """Overriding specification decorator base class"""
    __module__ = __name__
    __providedBy__ = DecoratorSpecificationDescriptor()
    __Security_checker__ = DecoratedSecurityCheckerDescriptor()


class DecoratorProvidesDescriptor(object):
    __module__ = __name__

    def __get__(self, inst, cls):
        if inst is None:
            return self
        return proxy.getProxiedObject(inst).__provides__

    def __set__(self, inst, value):
        proxy.getProxiedObject(inst).__provides__ = value

    def __delete__(self, inst):
        del proxy.getProxiedObject(inst).__provides__


def proxyImplements(cls, *interfaces):
    interface.classImplements(cls, *interfaces)
    if type(cls.__provides__) is not DecoratorProvidesDescriptor:
        cls.__provides__ = DecoratorProvidesDescriptor()


def implements(*interfaces):
    declarations._implements('implements', interfaces, proxyImplements)


class ClassAndInstanceDescr(object):
    __module__ = __name__

    def __init__(self, *args):
        self.funcs = args

    def __get__(self, inst, cls):
        if inst is None:
            return self.funcs[1](cls)
        return self.funcs[0](inst)

    def __set__(self, inst, v):
        raise TypeError('assignment not allowed')


class ProxyBase(proxy.ProxyBase):
    __module__ = __name__
    __slots__ = ('__traversed_parent__', '__traversed_name__')

    def __new__(self, ob, parent, name):
        return proxy.ProxyBase.__new__(self, ob)

    def __init__(self, ob, parent, name):
        proxy.ProxyBase.__init__(self, ob)
        self.__traversed_parent__ = parent
        self.__traversed_name__ = name

    __doc__ = ClassAndInstanceDescr(lambda inst: proxy.getProxiedObject(inst).__doc__, lambda cls, __doc__=__doc__: __doc__)
    __providedBy__ = DecoratorSpecificationDescriptor()
    __Security_checker__ = DecoratedSecurityCheckerDescriptor()


class Proxy(ProxyBase):
    __module__ = __name__
    implements(interfaces.ITraversalProxy)


class TargetProxy(ProxyBase):
    __module__ = __name__
    implements(interfaces.ITargetProxy)
    __slots__ = ('__shortcut__', )

    def __new__(self, ob, parent, name, shortcut):
        return ProxyBase.__new__(self, ob, parent, name)

    def __init__(self, ob, parent, name, shortcut):
        ProxyBase.__init__(self, ob, parent, name)
        self.__shortcut__ = shortcut


class ShortcutProxy(Proxy):
    __module__ = __name__

    @property
    def target(self):
        shortcut = proxy.getProxiedObject(self)
        return TargetProxy(shortcut.raw_target, self.__traversed_parent__, self.__traversed_name__, shortcut)


def removeProxy(obj):
    p = proxy.queryInnerProxy(obj, ProxyBase)
    if p is None:
        return obj
    else:
        return proxy.getProxiedObject(p)
    return