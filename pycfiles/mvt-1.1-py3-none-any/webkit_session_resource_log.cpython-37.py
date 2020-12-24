# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/webkit_session_resource_log.py
# Compiled at: 2020-02-21 06:08:45
# Size of source mod 2**32: 4551 bytes
import os, io, glob, sqlite3, logging, biplist
from .base import IOSExtraction
from ..utils import get_domain_from_url
from ..utils import convert_mactime_to_unix, convert_timestamp_to_iso
log = logging.getLogger(__name__)
WEBKIT_SESSION_RESOURCE_LOG_ROOT_PATHS = [
 'private/var/mobile/Containers/Data/Application/*/SystemData/com.apple.SafariViewService/Library/WebKit/WebsiteData/full_browsing_session_resourceLog.plist',
 'private/var/mobile/Containers/Data/Application/*/Library/WebKit/WebsiteData/ResourceLoadStatistics/full_browsing_session_resourceLog.plist',
 'private/var/mobile/Library/WebClips/*/Storage/full_browsing_session_resourceLog.plist']

class WebkitSessionResourceLog(IOSExtraction):
    __doc__ = 'This module extracts records from WebKit browsing session\n    resource logs, and checks them against any provided list of\n    suspicious domains.'

    def _extract(self, file_path):
        items = []
        file_plist = biplist.readPlist(file_path)
        if 'browsingStatistics' not in file_plist:
            return items
        browsing_stats = file_plist['browsingStatistics']
        for item in browsing_stats:
            items.append(dict(origin=(item['PrevalentResourceOrigin']),
              redirect_source=(item.get('topFrameUniqueRedirectsFrom')),
              redirect_destination=(item.get('topFrameUniqueRedirectsTo')),
              subframe_under_origin=(item.get('subframeUnderTopFrameOrigins')),
              subresource_under_origin=(item.get('subresourceUnderTopFrameOrigins')),
              user_interaction=(item['hadUserInteraction']),
              most_recent_interaction=(convert_timestamp_to_iso(item['mostRecentUserInteraction'])),
              last_seen=(convert_timestamp_to_iso(item['lastSeen']))))

        return items

    @staticmethod
    def _extract_sub_origins(origin_list):
        if not origin_list:
            return []
        return [origin['origin'] for origin in origin_list]

    def _find_suspect_domains(self, results):
        for result in results:
            source_origins = self._extract_sub_origins(result['redirect_source'])
            destination_origins = self._extract_sub_origins(result['redirect_destination'])
            subframe_origins = self._extract_sub_origins(result['subframe_under_origin'])
            subresource_origins = self._extract_sub_origins(result['subresource_under_origin'])
            all_origins = set([result['origin']] + source_origins + destination_origins)
            suspicious_found = self._check_domains(all_origins)
            if suspicious_found:
                redirect_path = ' -> '.join([
                 ', '.join(source_origins),
                 '*{}*'.format(result['origin']),
                 ', '.join(destination_origins)])
                log.info('Found HTTP redirect between suspicious domains: %s', redirect_path)

    def _find_paths(self, root_paths):
        results = {}
        for root_path in root_paths:
            for found_path in glob.glob(os.path.join(self.base_folder, root_path)):
                if not os.path.exists(found_path):
                    continue
                key = os.path.relpath(found_path, self.base_folder)
                if key not in results:
                    results[key] = []

        return results

    def run(self):
        self.results = self._find_paths(root_paths=WEBKIT_SESSION_RESOURCE_LOG_ROOT_PATHS)
        for log_file in self.results.keys():
            log.info('Found Safari browsing session resource log at path: %s', log_file)
            results = self._extract(os.path.join(self.base_folder, log_file))
            self._find_suspect_domains(results)
            self.results[log_file] = results