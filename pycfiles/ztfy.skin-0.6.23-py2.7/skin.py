# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/skin.py
# Compiled at: 2014-03-19 05:55:25
from z3c.formui.interfaces import IFormUILayer
from ztfy.skin.layer import IBaseZTFYLayer, IZTFYBrowserLayer, IZTFYBackLayer, IZTFYFrontLayer

class IBaseZTFYSkin(IFormUILayer, IBaseZTFYLayer):
    """The ZTFY browser skin, using a skin-based form layout"""
    pass


class IZTFYSkin(IBaseZTFYSkin, IZTFYBrowserLayer):
    """The ZTFY base JavaScript skin"""
    pass


class IZTFYBackSkin(IZTFYSkin, IZTFYBackLayer):
    """ZTFY back-office skin"""
    pass


class IZTFYFrontSkin(IZTFYSkin, IZTFYFrontLayer):
    """ZTFY front-office skin"""
    pass