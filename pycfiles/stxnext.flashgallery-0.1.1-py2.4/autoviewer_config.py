# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/stxnext/flashgallery/browser/autoviewer_config.py
# Compiled at: 2008-08-03 09:41:38
from simpleviewer_config import SimpleViewerConfig

class AutoViewerConfig(SimpleViewerConfig):
    """
    View class for autoviewer XML configure data. 
    """
    __module__ = __name__

    def getImageCaption(self, image):
        """
        Return caption of given image.
        """
        return '<font size="14">%s</font>' % super(AutoViewerConfig, self).getImageCaption(image)

    def getImageWidth(self, image):
        """
        Return image_large width.
        """
        try:
            return self.context.restrictedTraverse('%s/image_preview' % image.getId).width
        except:
            return 0

    def getImageHeight(self, image):
        """
        Return image_large width.
        """
        try:
            return self.context.restrictedTraverse('%s/image_preview' % image.getId).height
        except:
            return 0