# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/grelek/projects/onesignal-notifications/venv/lib/python3.7/site-packages/onesignal/device_notification.py
# Compiled at: 2019-03-19 08:10:19
# Size of source mod 2**32: 2701 bytes
from .notification import Notification, common_notification_paramenters
from .utils import merge_dicts

class DeviceNotification(Notification):
    'Notification to a specific device using their id\n\n    Attributes:\n        include_player_ids\n        include_external_user_ids\n        include_email_tokens\n        include_ios_tokens\n        include_wp_urls\n        include_wp_wns_uris\n        include_amazon_reg_ids\n        include_chrome_reg_ids\n        include_chrome_web_reg_ids\n        include_android_reg_ids\n        {common_notification_paramenters}\n    '.format(common_notification_paramenters=common_notification_paramenters)

    def __init__(self, include_player_ids=None, include_external_user_ids=None, include_email_tokens=None, include_ios_tokens=None, include_wp_urls=None, include_wp_wns_uris=None, include_amazon_reg_ids=None, include_chrome_reg_ids=None, include_chrome_web_reg_ids=None, include_android_reg_ids=None, **kwargs):
        (Notification.__init__)(self, **kwargs)
        self.include_player_ids = include_player_ids
        self.include_external_user_ids = include_external_user_ids
        self.include_email_tokens = include_email_tokens
        self.include_ios_tokens = include_ios_tokens
        self.include_wp_urls = include_wp_urls
        self.include_wp_wns_uris = include_wp_wns_uris
        self.include_amazon_reg_ids = include_amazon_reg_ids
        self.include_chrome_reg_ids = include_chrome_reg_ids
        self.include_chrome_web_reg_ids = include_chrome_web_reg_ids
        self.include_android_reg_ids = include_android_reg_ids

    def get_data(self):
        return merge_dicts(self.get_common_data(), {k:v for k, v in {'include_player_ids':self.include_player_ids, 
         'include_external_user_ids':self.include_external_user_ids, 
         'include_email_tokens':self.include_email_tokens, 
         'include_ios_tokens':self.include_ios_tokens, 
         'include_wp_urls':self.include_wp_urls, 
         'include_wp_wns_uris':self.include_wp_wns_uris, 
         'include_amazon_reg_ids':self.include_amazon_reg_ids, 
         'include_chrome_reg_ids':self.include_chrome_reg_ids, 
         'include_chrome_web_reg_ids':self.include_chrome_web_reg_ids, 
         'include_android_reg_ids':self.include_android_reg_ids}.items() if v is not None if v is not None})