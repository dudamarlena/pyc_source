# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/taar/profile_fetcher.py
# Compiled at: 2018-02-19 09:44:52
# Size of source mod 2**32: 1403 bytes
import logging
logger = logging.getLogger(__name__)

class ProfileFetcher(object):
    __doc__ = ' Fetch the latest information for a client on the backing\n    datastore\n    '

    def __init__(self, client):
        self.client = client

    def get(self, client_id):
        profile_data = self.client.get_client_profile(client_id)
        if profile_data is None:
            logger.error('Client profile not found', extra={'client_id': client_id})
            return
        addon_ids = [addon['addon_id'] for addon in profile_data['active_addons'] if not addon.get('is_system', False)]
        return {'geo_city': profile_data.get('city', ''), 
         'subsession_length': profile_data.get('subsession_length', 0), 
         'locale': profile_data.get('locale', ''), 
         'os': profile_data.get('os', ''), 
         'installed_addons': addon_ids, 
         'disabled_addons_ids': profile_data.get('disabled_addons_ids', []), 
         'bookmark_count': profile_data.get('places_bookmarks_count', 0), 
         'tab_open_count': profile_data.get('scalar_parent_browser_engagement_tab_open_event_count', 0), 
         'total_uri': profile_data.get('scalar_parent_browser_engagement_total_uri_count', 0), 
         'unique_tlds': profile_data.get('scalar_parent_browser_engagement_unique_domains_count', 0)}