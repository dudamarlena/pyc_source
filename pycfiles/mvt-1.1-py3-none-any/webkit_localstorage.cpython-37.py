# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/webkit_localstorage.py
# Compiled at: 2020-02-11 11:39:52
# Size of source mod 2**32: 1187 bytes
from .webkit_base import WebkitBase
WEBKIT_LOCALSTORAGE_ROOT_PATHS = [
 'private/var/mobile/Containers/Data/Application/*/Library/WebKit/WebsiteData/LocalStorage/']

class WebkitLocalstorage(WebkitBase):
    __doc__ = 'This module looks extracts records from WebKit LocalStorage folders,\n    and checks them against any provided list of suspicious domains.'

    def run(self):
        self.results = self._process_paths(WEBKIT_LOCALSTORAGE_ROOT_PATHS)