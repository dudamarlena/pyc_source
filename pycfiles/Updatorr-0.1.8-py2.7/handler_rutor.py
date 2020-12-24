# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/updatorr/tracker_handlers/handler_rutor.py
# Compiled at: 2013-02-17 00:08:25
from updatorr.handler_base import GenericPublicTrackerHandler
from updatorr.utils import register_tracker_handler

class RutorHandler(GenericPublicTrackerHandler):
    """This class implements .torrent files downloads
    for http://rutor.org tracker."""

    def get_download_link(self):
        """Tries to find .torrent file download link at forum thread page
        and return that one."""
        linkToFind = 'd.rutor.org/download/%s' % self.get_id_from_link()
        response, page_html = self.get_resource(self.resource_url)
        page_links = self.find_links(page_html)
        download_link = None
        for page_link in page_links:
            if linkToFind in page_link:
                download_link = page_link
                break

        return download_link


register_tracker_handler('rutor.org', RutorHandler)