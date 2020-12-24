# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/safari_favicon.py
# Compiled at: 2020-02-21 13:02:24
# Size of source mod 2**32: 3130 bytes
import os, sqlite3, logging, operator
from .base import IOSExtraction
from ..utils import get_domain_from_url
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso
log = logging.getLogger(__name__)
SAFARI_FAVICON_ROOT_PATHS = [
 'private/var/mobile/Library/Image Cache/Favicons/Favicons.db',
 'private/var/mobile/Containers/Data/Application/*/Library/Image Cache/Favicons/Favicons.db']

class SafariFavicon(IOSExtraction):
    __doc__ = "This module extracts all Safari favicon records.\n\n    Note: as of iOS 13 Safari's database file is no longer exported by iTunes."

    def _extract(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT\n                page_url.url,\n                icon_info.url,\n                icon_info.timestamp\n            FROM page_url\n            JOIN icon_info ON page_url.uuid = icon_info.uuid\n            ORDER BY icon_info.timestamp;')
        items = []
        for item in cur:
            items.append(dict(url=(item[0]),
              icon_url=(item[1]),
              timestamp=(item[2]),
              isodate=(convert_timestamp_to_iso(convert_mactime_to_unix(item[2]))),
              type='valid'))

        cur.execute('SELECT\n                page_url,\n                icon_url,\n                timestamp\n            FROM rejected_resources ORDER BY timestamp;')
        for item in cur:
            items.append(dict(url=(item[0]),
              icon_url=(item[1]),
              timestamp=(item[2]),
              isodate=(convert_timestamp_to_iso(convert_mactime_to_unix(item[2]))),
              type='rejected'))

        cur.close()
        conn.close()
        log.info('Extracted a total of %d favicon records', len(items))
        self.results = sorted(items, key=(lambda item: item['isodate']))

    def _find_domains(self):
        for result in self.results:
            self._check_domains([result['url']])
            self._check_domains([result['icon_url']])

    def run(self):
        self._find_database(root_paths=SAFARI_FAVICON_ROOT_PATHS)
        log.info('Found Safari favicon cache database at path: %s', self.file_path)
        self._extract()
        self._find_domains()