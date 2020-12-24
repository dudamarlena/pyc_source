# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/updatorr/tracker_handlers/handler_anidub.py
# Compiled at: 2013-02-16 23:57:33
from updatorr.handler_base import GenericPrivateTrackerHandler
from updatorr.utils import register_tracker_handler
import urllib2

class AnidubHandler(GenericPrivateTrackerHandler):
    """This class implements .torrent files downloads
    for http://tr.anidub.com tracker."""
    login_url = 'http://tr.anidub.com/takelogin.php'
    cookie_logged_in = 'uid'

    def get_download_link(self):
        """Tries to find .torrent file download link at forum thread page
        and return that one."""
        response, page_html = self.get_resource(self.resource_url)
        page_links = self.find_links(page_html)
        download_link = None
        for page_link in page_links:
            if 'login.php?returnto=' in page_link:
                download_link = None
                self.debug('Login is required to download torrent file.')
                if self.login(self.get_settings('login'), self.get_settings('password')):
                    download_link = self.get_download_link()
            if 'download.php?id=' in page_link:
                download_link = 'http://tr.anidub.com/%s' % urllib2.unquote(page_link).replace('&amp;', '&')

        return download_link


register_tracker_handler('tr.anidub.com', AnidubHandler)