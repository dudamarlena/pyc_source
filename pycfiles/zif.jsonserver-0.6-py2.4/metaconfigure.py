# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/metaconfigure.py
# Compiled at: 2007-05-25 16:54:17
"""JSON-RPC configuration code

like zope.app.publisher.xmlrpc.metaconfigure

registerAdapter vs provideAdapter jwashin 20060525
updated 2005-12-03 Roger Ineichen
jwashin 2005-06-06

"""
import zope.interface
from zope.interface import Interface
from zope.security.checker import CheckerPublic, Checker
from zope.configuration.exceptions import ConfigurationError
from interfaces import IJSONRPCRequest
from zope.component.interface import provideInterface
from zope.app.component.metaconfigure import handler
from jsonrpc import MethodPublisher

def view(_context, for_=None, interface=None, methods=None, class_=None, permission=None, name=None):
    interface = interface or []
    methods = methods or []
    if permission == 'zope.Public':
        permission = CheckerPublic
    require = {}
    for attr_name in methods:
        require[attr_name] = permission

    if interface:
        for iface in interface:
            for field_name in iface:
                require[field_name] = permission

            _context.action(discriminator=None, callable=provideInterface, args=('', for_))

    if class_ is None:
        class_ = MethodPublisher
        original_class = class_
    else:
        original_class = class_
        class_ = type(class_.__name__, (class_, MethodPublisher), {})
    if name:
        if permission:
            checker = Checker(require)

            def proxyView(context, request, class_=class_, checker=checker):
                view = class_(context, request)
                view.__Security_checker__ = checker
                return view

            class_ = proxyView
            class_.factory = original_class
        _context.action(discriminator=('view', for_, name, IJSONRPCRequest), callable=handler, args=('registerAdapter', class_, (for_, IJSONRPCRequest), Interface, name, _context.info))
    elif permission:
        checker = Checker({'__call__': permission})
    else:
        checker = None
    for name in require:
        cdict = {'__Security_checker__': checker, '__call__': getattr(class_, name)}
        new_class = type(class_.__name__, (class_,), cdict)
        _context.action(discriminator=('view', for_, name, IJSONRPCRequest), callable=handler, args=('registerAdapter', new_class, (for_, IJSONRPCRequest), Interface, name, _context.info))

    if for_ is not None:
        _context.action(discriminator=None, callable=provideInterface, args=('', for_))
    return