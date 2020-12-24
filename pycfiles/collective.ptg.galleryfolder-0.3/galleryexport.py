# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/zinstance/src/collective.ptg.galleryfolder/collective/ptg/galleryfolder/browser/galleryexport.py
# Compiled at: 2012-12-21 06:03:56
import os, tempfile, zipfile
from Products.Five import BrowserView
from tempfile import TemporaryFile

class Exporter(BrowserView):

    def __init__(self, context, request):
        super(Exporter, self).__init__(context, request)

    def __call__(self, REQUEST):
        """Returns the file (with the 'scaled' images
        """
        imagesize = self.request.get('imagesize', 'none')
        zip_filename = tempfile.mktemp()
        ZIP = zipfile.ZipFile(zip_filename, 'w')
        for obj in self.context.getFolderContents():
            obj = obj.getObject()
            imageformat = obj.getContentType()
            imageformat = imageformat.split('/')
            image_suffix = imageformat[1]
            if image_suffix == 'jpeg':
                image_suffix = 'jpg'
            if obj.portal_type == 'Image':
                full_image_name = obj.getId() + '.' + image_suffix
                if imagesize == 'none':
                    img = obj.getImage()
                else:
                    img = obj.Schema().getField('image').getScale(obj, scale=imagesize)
                ZIP.writestr(self.context.getId() + '/' + full_image_name, str(img.data))

        ZIP.close()
        data = file(zip_filename).read()
        os.unlink(zip_filename)
        R = self.request.RESPONSE
        R.setHeader('content-type', 'application/zip')
        R.setHeader('content-length', len(data))
        R.setHeader('content-disposition', 'attachment; filename="%s.zip"' % self.context.getId())
        return R.write(data)