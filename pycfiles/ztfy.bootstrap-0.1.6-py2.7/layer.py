# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/bootstrap/layer.py
# Compiled at: 2013-02-23 03:40:02
__docformat__ = 'restructuredtext'
from ztfy.skin.layer import IZTFYFrontLayer
from ztfy.skin.skin import IZTFYFrontSkin
from zope.schema import TextLine
from ztfy.bootstrap import _

class IBootstrapLayer(IZTFYFrontLayer):
    """Bootstrap layer"""
    pass


class IBootstrapSkin(IZTFYFrontSkin, IBootstrapLayer):
    """Bootstrap skin"""
    label = TextLine(title=_('Bootstrap skin'))