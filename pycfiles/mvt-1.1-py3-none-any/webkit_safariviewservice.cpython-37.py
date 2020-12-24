# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/webkit_safariviewservice.py
# Compiled at: 2020-02-19 11:24:12
# Size of source mod 2**32: 1218 bytes
from .webkit_base import WebkitBase
WEBKIT_LOCALSTORAGE_ROOT_PATHS = [
 'private/var/mobile/Containers/Data/Application/*/SystemData/com.apple.SafariViewService/Library/WebKit/WebsiteData/']

class WebkitSafariViewService(WebkitBase):
    __doc__ = 'This module looks extracts records from WebKit LocalStorage folders,\n    and checks them against any provided list of suspicious domains.'

    def run(self):
        self.results = self._process_paths(WEBKIT_LOCALSTORAGE_ROOT_PATHS)