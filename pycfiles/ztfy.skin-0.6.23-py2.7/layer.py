# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/skin/layer.py
# Compiled at: 2014-03-19 06:21:46
from jquery.layer import IJQueryJavaScriptBrowserLayer
from ztfy.baseskin.layer import IBaseSkinLayer

class IBaseZTFYLayer(IBaseSkinLayer):
    """ZTFY base layer"""
    pass


class IZTFYBrowserLayer(IBaseZTFYLayer, IJQueryJavaScriptBrowserLayer):
    """ZTFY JavaScript layer"""
    pass


class IZTFYBackLayer(IZTFYBrowserLayer):
    """ZTFY back-office layer"""
    pass


class IZTFYFrontLayer(IZTFYBrowserLayer):
    """ZTFY front-office layer"""
    pass