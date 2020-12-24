# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmi/layer.py
# Compiled at: 2012-06-20 12:11:31
__docformat__ = 'restructuredtext'
from zope.app.basicskin import IDefaultBrowserLayer
from ztfy.skin.layer import IZTFYBackLayer
from ztfy.skin.skin import IZTFYBackSkin

class IZMILayer(IZTFYBackLayer, IDefaultBrowserLayer):
    """ZMI layer interface"""
    pass


class IZMISkin(IZTFYBackSkin, IZMILayer):
    """ZMI skin interface"""
    pass