# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/claeyswo/Envs/env_oe_utils/lib/python3.6/site-packages/oe_utils/scripts/archive_feed.py
# Compiled at: 2019-06-18 07:34:37
# Size of source mod 2**32: 1087 bytes
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import logging, requests
log = logging.getLogger(__name__)

def archive_entries(feed_list, session, system_token):
    for feed_obj in feed_list:
        atom_feed_manager = feed_obj['atom_feed_manager'](session, feed_obj['atom_feed_folder'])
        archive_feed_url = feed_obj['archive_feed_url']
        max_entries = feed_obj['max_entries']
        current_feed = atom_feed_manager.current_feed
        entries_count = len(current_feed.entries)
        log.debug('Number of entries: {}'.format(entries_count))
        if entries_count >= max_entries:
            log.debug('Archive current feed')
            archive_feed = requests.post(archive_feed_url,
              headers={'OpenAmSSOID':system_token,  'Accept':'Application/json'})
            if archive_feed.status_code != 200:
                log.error('Failed to archive on url {}'.format(archive_feed_url))
                archive_feed.raise_for_status()