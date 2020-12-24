# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/net_datausage.py
# Compiled at: 2020-02-11 11:39:52
# Size of source mod 2**32: 1401 bytes
import logging
from .net_base import NetBase
log = logging.getLogger(__name__)
DATAUSAGE_BACKUP_ID = '0d609c54856a9bb2d56729df1d68f2958a88426b'
DATAUSAGE_ROOT_PATHS = [
 'private/var/wireless/Library/Databases/DataUsage.sqlite']

class Datausage(NetBase):
    __doc__ = 'This class extracts data from DataUsage.sqlite and attempts to identify\n    any suspicious processes if running on a full filesystem dump.'

    def run(self):
        self._find_database(backup_id=DATAUSAGE_BACKUP_ID, root_paths=DATAUSAGE_ROOT_PATHS)
        log.info('Found DataUsage database at path: %s', self.file_path)
        self._extract()
        self._find_suspicious_processes()