# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/net_base.py
# Compiled at: 2020-02-21 08:16:28
# Size of source mod 2**32: 3497 bytes
import os, sqlite3, logging
from pathlib import Path
from .base import IOSExtraction
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso
log = logging.getLogger(__name__)

class NetBase(IOSExtraction):
    __doc__ = 'This class provides a base for DataUsage and NetUsage extraction modules.'

    def _extract(self):
        conn = sqlite3.connect(self.file_path)
        cur = conn.cursor()
        cur.execute('SELECT\n                ZPROCESS.ZFIRSTTIMESTAMP,\n                ZPROCESS.ZTIMESTAMP,\n                ZPROCESS.ZPROCNAME,\n                ZPROCESS.ZBUNDLENAME,\n                ZLIVEUSAGE.ZWIFIIN,\n                ZLIVEUSAGE.ZWIFIOUT,\n                ZLIVEUSAGE.ZWWANIN,\n                ZLIVEUSAGE.ZWWANOUT,\n                ZLIVEUSAGE.Z_PK\n            FROM ZLIVEUSAGE\n            LEFT JOIN ZPROCESS ON ZLIVEUSAGE.ZHASPROCESS = ZPROCESS.Z_PK;')
        items = []
        for item in cur:
            items.append(dict(first_isodate=(convert_timestamp_to_iso(convert_mactime_to_unix(item[0]))),
              last_isodate=(convert_timestamp_to_iso(convert_mactime_to_unix(item[1]))),
              proc_name=(item[2]),
              bundle_id=(item[3]),
              wifi_in=(item[4]),
              wifi_out=(item[5]),
              wwan_in=(item[6]),
              wwan_out=(item[7]),
              proc_id=(item[8])))

        cur.close()
        conn.close()
        log.info('Extracted information on %d processes', len(items))
        self.results = items

    def _find_suspicious_processes(self):
        if not self.root:
            return
        log.info('Looking for suspicious processes...')
        files = []
        for posix_path in Path(self.base_folder).rglob('*'):
            if not posix_path.is_file():
                continue
            files.append([posix_path.name, posix_path.__str__()])

        for proc in self.results:
            if not proc['bundle_id']:
                log.debug('Found process with no Bundle ID with name: %s', proc['proc_name'])
                binary_path = None
                for file in files:
                    if proc['proc_name'] == file[0]:
                        binary_path = file[1]
                        break

                if binary_path:
                    log.debug('Located at %s', binary_path)
                else:
                    msg = 'Could not find the binary associated with the process with name {}'.format(proc['proc_name'])
                    if len(proc['proc_name']) == 16:
                        msg = msg + ' (However, the process name might have been truncated in the database)'
                    log.warning(msg)