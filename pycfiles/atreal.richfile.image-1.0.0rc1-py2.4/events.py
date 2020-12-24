# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/image/events.py
# Compiled at: 2009-09-04 10:39:07
from zope.interface.interfaces import IInterface
from zope.component import queryUtility
from atreal.richfile.image.interfaces import IImageable

def is_richfileimage_installed():
    """
    """
    return queryUtility(IInterface, name='atreal.richfile.image.IRichFileImageSite', default=False)


def buildAndStoreImage(obj, event):
    """
    """
    if not is_richfileimage_installed():
        return
    print 'atreal.richfile.image: build and store image for %s' % (('/').join(obj.getPhysicalPath()),)
    IImageable(obj).process()


def cleanImageData(obj, event):
    """
    """
    if not is_richfileimage_installed():
        return
    print 'atreal.richfile.image: clean data for %s' % (('/').join(obj.getPhysicalPath()),)
    IImageable(obj).cleanUp()