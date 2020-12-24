# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/skin/menu.py
# Compiled at: 2013-03-15 02:59:45
__docformat__ = 'restructuredtext'
from ztfy.gallery.skin.layer import IGallerySkin
from ztfy.skin.menu import SkinTargetMenuItem, SkinTargetJsMenuItem, SkinTargetDialogMenuItem

class GallerySkinMenuItem(SkinTargetMenuItem):
    skin = IGallerySkin


class GallerySkinJsMenuItem(SkinTargetJsMenuItem):
    skin = IGallerySkin


class GallerySkinDialogMenuItem(SkinTargetDialogMenuItem):
    skin = IGallerySkin