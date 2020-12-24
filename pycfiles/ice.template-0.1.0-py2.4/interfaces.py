# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ice/template/tests/interfaces.py
# Compiled at: 2009-05-04 14:30:04
from z3c.form.interfaces import IFormLayer
from z3c.formui.interfaces import IDivFormLayer
from z3c.layer.pagelet import IPageletBrowserLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ILayer(IFormLayer, IPageletBrowserLayer):
    """Layer"""
    __module__ = __name__


class ISkin(IDivFormLayer, ILayer, IDefaultBrowserLayer):
    """Skin Layer"""
    __module__ = __name__