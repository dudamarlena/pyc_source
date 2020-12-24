# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/theme/browser/publication_display.py
# Compiled at: 2018-04-23 08:38:48
from Products.Five.browser import BrowserView

class PublicationDisplay(BrowserView):

    def __call__(self):
        try:
            image = self.context.image.image_thumb
            safe_title = self.context.title.decode('utf-8', 'replace')
            image.title = safe_title
            image.alt = safe_title
            return image
        except AttributeError:
            return