# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/updatorr/tracker_handlers/handler_rutracker.py
# Compiled at: 2013-02-16 23:56:02
from updatorr.handler_base import GenericPrivateTrackerHandler
from updatorr.utils import register_tracker_handler

class RutrackerHandler(GenericPrivateTrackerHandler):
    """This class implements .torrent files downloads
    for http://rutracker.org tracker."""
    login_url = 'http://login.rutracker.org/forum/login.php'
    cookie_logged_in = 'bb_data'

    def get_login_form_data(self, login, password):
        """Returns a dictionary with data to be pushed to authorization form."""
        return {'login_username': login, 'login_password': password, 'login': 'pushed'}

    def before_download(self):
        """Used to perform some required actions right before .torrent download."""
        self.set_cookie('bb_dl', self.get_id_from_link())

    def get_download_link(self):
        """Tries to find .torrent file download link at forum thread page
        and return that one."""
        response, page_html = self.get_resource(self.resource_url)
        page_links = self.find_links(page_html)
        download_link = None
        for page_link in page_links:
            if 'dl.rutracker.org' in page_link:
                download_link = page_link
                if 'guest' in download_link:
                    download_link = None
                    self.debug('Login is required to download torrent file.')
                    if self.login(self.get_settings('login'), self.get_settings('password')):
                        download_link = self.get_download_link()
                break

        return download_link


register_tracker_handler('rutracker.org', RutrackerHandler)