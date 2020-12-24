# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/smartimage/smartimagecache/smartimagecache.py
# Compiled at: 2008-12-23 17:55:58
"""SmartImageCache class for the Zope 3 based smartimage package

$Id: smartimagecache.py 35335 2008-05-27 16:02:13Z anatoly $
"""
__author__ = 'Anton Oprya'
__license__ = 'ZPL'
__version__ = '$Revision: 35335 $'
__date__ = '$Date: 2008-05-27 19:02:13 +0300 (Tue, 27 May 2008) $'
from zope.interface import implements
from interfaces import IScale, ISmartImageProp, ISmartImageCacheContainer, IStat
from zope.app.container.btree import BTreeContainer
from PIL import Image
from scale import Scale

class SmartImageCache(BTreeContainer):
    __module__ = __name__
    implements(ISmartImageProp, ISmartImageCacheContainer, IStat)
    scales = ()
    format = 'JPEG'
    mode = 'RGB'
    maxratio = 100.0
    interval = 900
    iscached = True
    elementsamount = 0
    elementssize = 0.0
    meansize = 0.0
    resample = Image.ANTIALIAS
    quality = 90
    scale = ''
    basepath = ''
    use_basepath = False