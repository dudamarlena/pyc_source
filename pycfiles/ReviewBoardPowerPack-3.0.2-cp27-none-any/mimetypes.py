# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/pdf/mimetypes.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import division
import logging
try:
    import Image
except ImportError:
    from PIL import Image

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import escape, mark_safe
from djblets.util.templatetags.djblets_images import save_image_to_storage
from reviewboard.attachments.mimetypes import MimetypeHandler
from rbpowerpack.pdf.utils import convert_data_uri_to_image, get_pdf_worker_url
from rbpowerpack.utils.extension import get_powerpack_extension

class PDFMimetype(MimetypeHandler):
    """Handles PDF mimetypes."""
    supported_mimetypes = [
     'application/pdf', 'application/x-pdf']
    SD_THUMBNAIL_WIDTH = 400
    SD_THUMBNAIL_HEIGHT = 100
    HD_THUMBNAIL_WIDTH = 600

    def __init__(self, attachment, mimetype):
        super(PDFMimetype, self).__init__(attachment, mimetype)
        if not hasattr(self, 'use_hd_thumbnails'):
            self.use_hd_thumbnails = False
        filename = attachment.orig_filename
        if not filename:
            filename = attachment.file.name
        if not filename.lower().endswith('.pdf'):
            raise Exception('PDFMimetype: rejecting document %s because of incorrect extension' % filename)

    def get_thumbnail_filename(self):
        if self.use_hd_thumbnails:
            return '%s_%d.png' % (self.attachment.file.name,
             self.HD_THUMBNAIL_WIDTH)
        else:
            return '%s_%dx%d.png' % (self.attachment.file.name,
             self.SD_THUMBNAIL_WIDTH,
             self.SD_THUMBNAIL_HEIGHT)

    def get_thumbnail(self):
        """Returns a thumbnail of the document."""
        storage = self.attachment.file.storage
        filename = self.get_thumbnail_filename()
        if storage.exists(filename):
            if self.use_hd_thumbnails:
                return mark_safe('<div class="file-thumbnail"> <img src="%s" class="pdf-thumbnail-hd" alt="%s" /></div>' % (
                 storage.url(filename), escape(self.attachment.caption)))
            else:
                return mark_safe('<img src="%s" class="pdf-thumbnail-sd" alt="%s" />' % (
                 storage.url(filename), escape(self.attachment.caption)))

        else:
            extension = get_powerpack_extension()
            return mark_safe(render_to_string('powerpack/pdf-thumbnailer.html', {'pdf': self.attachment, 
               'extension': extension, 
               'pdf_worker_url': get_pdf_worker_url(extension), 
               'MEDIA_URL': settings.MEDIA_URL}))

    def set_thumbnail(self, data):
        """Set the thumbnail from the given data.

        This saves the thumbnail based on the data that's sent via the API. We
        do some checking to verify that the image is in a valid format and then
        save it to storage."""
        try:
            image = convert_data_uri_to_image(data)
            if self.use_hd_thumbnails:
                width = self.HD_THUMBNAIL_WIDTH
                height = width * (image.size[1] / image.size[0])
            else:
                width = self.SD_THUMBNAIL_WIDTH
                height = self.SD_THUMBNAIL_HEIGHT
            image.thumbnail([width, height], Image.ANTIALIAS)
            save_image_to_storage(image, self.attachment.file.storage, self.get_thumbnail_filename())
        except Exception as e:
            logging.error('Failed to convert data uri to image: %s.' % e)
            raise e