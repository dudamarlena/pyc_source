# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/safari_history.py
# Compiled at: 2020-02-21 08:16:00
# Size of source mod 2**32: 4290 bytes
import os, sqlite3, logging
from .base import IOSExtraction
from ..utils import get_domain_from_url
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso
log = logging.getLogger(__name__)
SAFARI_HISTORY_BACKUP_ID = 'e74113c185fd8297e140cfcf9c99436c5cc06b57'
SAFARI_HISTORY_ROOT_PATHS = [
 'private/var/mobile/Library/Safari/History.db',
 'private/var/mobile/Containers/Data/Application/*/Library/Safari/History.db']

class SafariHistory(IOSExtraction):
    __doc__ = "This module extracts all Safari visits and tries to detect potential\n    network injection attacks.\n\n    Note: as of iOS 13 Safari's database file is no longer exported by iTunes."

    def _extract(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT\n                history_items.id,\n                history_items.url,\n                history_visits.id,\n                history_visits.visit_time,\n                history_visits.redirect_source,\n                history_visits.redirect_destination\n            FROM history_items\n            JOIN history_visits ON history_visits.history_item = history_items.id\n            ORDER BY history_visits.visit_time;')
        items = []
        for item in cur:
            items.append(dict(id=(item[0]),
              url=(item[1]),
              visit_id=(item[2]),
              timestamp=(item[3]),
              isodate=(convert_timestamp_to_iso(convert_mactime_to_unix(item[3]))),
              redirect_source=(item[4]),
              redirect_destination=(item[5])))

        cur.close()
        conn.close()
        log.info('Extracted a total of %d history items', len(items))
        self.results = items

    def _find_injections(self):
        for result in self.results:
            self._check_domains([result['url']])
            if not result['url'].lower().startswith('http://'):
                continue
            if not result['redirect_destination']:
                continue
            origin_domain = get_domain_from_url(result['url'])
            for redirect in self.results:
                if redirect['visit_id'] != result['redirect_destination']:
                    continue
                redirect_domain = get_domain_from_url(redirect['url'])
                if origin_domain == redirect_domain:
                    continue
                log.info('Found HTTP redirect to different domain: %s -> %s', origin_domain, redirect_domain)
                redirect_time = convert_mactime_to_unix(redirect['timestamp'])
                origin_time = convert_mactime_to_unix(result['timestamp'])
                elapsed_time = redirect_time - origin_time
                elapsed_ms = elapsed_time.microseconds / 1000
                if elapsed_time.seconds == 0:
                    log.warning('Redirect took less than a second! (%d milliseconds)', elapsed_ms)

    def run(self):
        self._find_database(backup_id=SAFARI_HISTORY_BACKUP_ID, root_paths=SAFARI_HISTORY_ROOT_PATHS)
        log.info('Found Safari history database at path: %s', self.file_path)
        self._extract()
        self._find_injections()