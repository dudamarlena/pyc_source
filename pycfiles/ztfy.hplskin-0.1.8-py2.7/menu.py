# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/hplskin/menu.py
# Compiled at: 2013-03-15 03:00:08
__docformat__ = 'restructuredtext'
from ztfy.hplskin.layer import IHPLSkin
from ztfy.skin.menu import SkinTargetMenuItem, SkinTargetJsMenuItem, SkinTargetDialogMenuItem

class HPLSkinMenuItem(SkinTargetMenuItem):
    """Customized menu item for ZBlog skin targets"""
    skin = IHPLSkin


class HPLSkinJsMenuItem(SkinTargetJsMenuItem):
    """Customized menu item for ZBlog skin targets"""
    skin = IHPLSkin


class HPLSkinDialogMenuItem(SkinTargetDialogMenuItem):
    """Customized menu item for ZBlog skin targets"""
    skin = IHPLSkin