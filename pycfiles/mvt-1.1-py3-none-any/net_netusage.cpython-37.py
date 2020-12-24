# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/net_netusage.py
# Compiled at: 2020-02-11 11:39:52
# Size of source mod 2**32: 1280 bytes
import logging
from .net_base import NetBase
log = logging.getLogger(__name__)
NETUSAGE_ROOT_PATHS = [
 'private/var/networkd/netusage.sqlite']

class Netusage(NetBase):
    __doc__ = 'This class extracts data from netusage.sqlite and attempts to identify\n    any suspicious processes if running on a full filesystem dump.'

    def run(self):
        self._find_database(root_paths=NETUSAGE_ROOT_PATHS)
        log.info('Found NetUsage database at path: %s', self.file_path)
        self._extract()
        self._find_suspicious_processes()