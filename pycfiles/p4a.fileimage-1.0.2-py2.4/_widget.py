# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/fileimage/image/_widget.py
# Compiled at: 2007-11-30 08:40:44
from zope.app.form.browser import widget
from p4a.fileimage import file

class ImageDisplayWidget(file.FileDownloadWidget):
    """Widget capable of displaying an image file.
    """
    __module__ = __name__

    @property
    def base_url(self):
        contentobj = self.context.context.context
        return contentobj.absolute_url() + '/viewimage'

    def __call__(self):
        if not self._data:
            return widget.renderElement('span', cssClass='image-absent', contents='No image set')
        url = self.url
        field = self.context
        extra = {}
        return widget.renderElement('img', src=url, **extra)


class ImageURLWidget(file.FileDownloadWidget):
    """Widget that returns the URL of the image
       This is clearly overkill, but it was the easy way to get
       something working fast.
       Revisit the consumer of this class and probably 
       access the url inline there.
    """
    __module__ = __name__

    @property
    def base_url(self):
        contentobj = self.context.context.context
        return contentobj.absolute_url() + '/viewimage'

    def __call__(self):
        if not self._data:
            return widget.renderElement('span', cssClass='image-absent', contents='No image set')
        return self.url