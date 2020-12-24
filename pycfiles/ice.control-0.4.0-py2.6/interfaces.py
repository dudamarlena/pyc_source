# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/skin/interfaces.py
# Compiled at: 2010-08-27 06:32:04
from z3c.form.interfaces import IFormLayer
from z3c.layer.pagelet import IPageletBrowserLayer
from z3c.formui.interfaces import IDivFormLayer
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

class ILayer(IFormLayer, IPageletBrowserLayer, IDefaultBrowserLayer):
    """Pretty admin UI layer for BlueBream."""
    pass


class ISkin(IDivFormLayer, ILayer):
    """Pretty admin UI skin for BlueBream"""
    pass