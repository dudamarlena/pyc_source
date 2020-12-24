# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/safari_browserstate.py
# Compiled at: 2020-02-21 13:09:07
# Size of source mod 2**32: 3602 bytes
import io, os, sqlite3, logging, operator, biplist
from .base import IOSExtraction
from ..utils import get_domain_from_url
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso
from ..utils import keys_bytes_to_string
log = logging.getLogger(__name__)
SAFARI_BROWSER_STATE_ROOT_PATHS = [
 'private/var/mobile/Library/Safari/BrowserState.db',
 'private/var/mobile/Containers/Data/Application/*/Library/Safari/BrowserState.db']

class SafariBrowserState(IOSExtraction):
    __doc__ = "This module extracts all Safari browser state records.\n\n    Note: as of iOS 13 Safari's database file is no longer exported by iTunes."

    def _extract(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT\n                tabs.title,\n                tabs.url,\n                tabs.user_visible_url,\n                tabs.last_viewed_time,\n                tab_sessions.session_data\n            FROM tabs\n            JOIN tab_sessions ON tabs.uuid = tab_sessions.tab_uuid\n            ORDER BY tabs.last_viewed_time;')
        session_history_count = 0
        items = []
        for item in cur:
            session_plist = item[4][4:]
            session_data = biplist.readPlist(io.BytesIO(session_plist))
            session_data = keys_bytes_to_string(session_data)
            session_entries = []
            for session_entry in session_data['SessionHistory']['SessionHistoryEntries']:
                session_history_count += 1
                session_entries.append(dict(entry_title=(session_entry['SessionHistoryEntryOriginalURL']),
                  entry_url=(session_entry['SessionHistoryEntryURL']),
                  data_length=(len(session_entry['SessionHistoryEntryData']))))

            items.append(dict(tab_title=(item[0]),
              tab_url=(item[1]),
              tab_visible_url=(item[2]),
              last_viewed_timestamp=(convert_timestamp_to_iso(convert_mactime_to_unix(item[3]))),
              session_data=session_entries))

        log.info('Extracted a total of %d tab records and %d session history entries', len(items), session_history_count)
        self.results = items

    def _find_domains(self):
        for result in self.results:
            self._check_domains([result['tab_url']])
            for session_entry in result['session_data']:
                self._check_domains([session_entry['entry_url']])

    def run(self):
        self._find_database(root_paths=SAFARI_BROWSER_STATE_ROOT_PATHS)
        log.info('Found Safari browser state database at path: %s', self.file_path)
        self._extract()
        self._find_domains()