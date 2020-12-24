# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_pagelet/metaconfigure.py
# Compiled at: 2020-02-20 08:01:50
# Size of source mod 2**32: 2304 bytes
"""PyAMS_pagelet.metaconfigure module

This module provides handlers for ZCML directives.
"""
from pyramid.exceptions import ConfigurationError
from pyramid.interfaces import IRequest
from pyramid_zcml import with_context
from zope.component import zcml
from zope.component.interface import provideInterface
from zope.interface import Interface, classImplements
from pyams_pagelet.interfaces import IPagelet
from pyams_pagelet.pagelet import Pagelet

def PageletDirective(_context, name, view, context=Interface, permission=None, layer=IRequest, **kwargs):
    """Pagelet ZCML directive"""
    if not view:
        raise ConfigurationError('You must specify a view class or interface')
    cdict = {'__name__': name, 
     'permission': permission}
    cdict.update(kwargs)
    new_class = type(view.__name__, (view, Pagelet), cdict)
    classImplements(new_class, IPagelet)
    _handle_for(_context, context)
    _context.action(discriminator=('pagelet', context, layer, name), callable=zcml.handler, args=(
     'registerAdapter', new_class,
     (
      context, layer),
     IPagelet, name, _context.info))
    config = with_context(_context)
    config.add_view(name=name, view=new_class, context=context, permission=permission, request_type=layer)


def _handle_for(_context, for_):
    if for_ is not None:
        _context.action(discriminator=None, callable=provideInterface, args=(
         '', for_))