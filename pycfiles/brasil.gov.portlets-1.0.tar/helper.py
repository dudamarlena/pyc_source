# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/browser/helper.py
# Compiled at: 2018-11-30 15:01:51
__doc__ = 'Helper view to return a background image or video to be used in the\nsite root when the expandable header is enabled.\n'
from __future__ import absolute_import
from brasil.gov.portal.controlpanel.portal import ISettingsPortal
from plone import api
from plone.formwidget.namedfile.converter import b64decode_file
from plone.namedfile.browser import Download
from plone.namedfile.file import NamedFile
import hashlib

class BackgroundMediaView(Download):
    """Helper view to return a background image or video to be used in
    the site root when the expandable header is enabled.
    """

    def setup(self):
        name = ISettingsPortal.__identifier__ + '.background_image'
        background_image = api.portal.get_registry_record(name, default=None)
        if background_image is None:
            self.data = None
            return
        else:
            filename, data = b64decode_file(background_image)
            self.filename = filename
            self.data = NamedFile(data=data, filename=filename)
            self.checksum = hashlib.sha1(data).hexdigest()
            return

    def _getFile(self):
        return self.data

    def __call__(self):
        """Render the background image or video.

        Make use of HTTP caching headers to decrease server usage:
        file is not cached on browsers and is cached 120 seconds on
        intermediate caches. We use a checksum of the image data as
        ETag to return a 304 (Not Modified) status in case the file
        has not changed since last time it was accessed.

        More information: https://httpwg.org/specs/rfc7234.html
        """
        self.setup()
        if self.data is None:
            self.request.RESPONSE.setStatus(410)
            return ''
        else:
            self.request.RESPONSE.setHeader('Cache-Control', 'max-age=0, s-maxage=120')
            self.request.RESPONSE.setHeader('ETag', self.checksum)
            match = self.request.get_header('If-None-Match', '')
            if self.checksum == match:
                self.request.response.setStatus(304)
                return ''
            return super(BackgroundMediaView, self).__call__()