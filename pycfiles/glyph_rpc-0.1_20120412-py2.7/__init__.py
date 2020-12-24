# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/glyph/__init__.py
# Compiled at: 2012-03-18 14:23:37
""" glyph-rpc - websites for robots """
from .data import CONTENT_TYPE, dump, parse, get, node, form, link, utcnow
from .resource.handler import safe, inline, redirect
from .resource.transient import TransientResource
from .resource.persistent import PersistentResource
from .resource.router import Router
from .server import Server
__all__ = [
 'CONTENT_TYPE', 'Server', 'redirect',
 'get', 'Router', 'Resource', 'r', 'safe', 'inline', 'utcnow',
 'parse', 'dump', 'node', 'form', 'link',
 'TransientResource', 'PersistentResource']
r = Resource = TransientResource