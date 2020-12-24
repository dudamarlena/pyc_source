# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/javed/Work/Dinette/forum/dinette/extra_settings.py
# Compiled at: 2013-07-02 04:51:32
import os
TOPIC_PAGE_SIZE = 3
REPLY_PAGE_SIZE = 3
AUTH_PROFILE_MODULE = 'dinette.DinetteUserProfile'
RANKS_NAMES_DATA = (
 (30, 'Member'), (100, 'Senior Member'), (300, 'Star'))
DINETTE_LOGIN_TEMPLATE = 'dinette/social_login.html'
LOG_FILE_PATH = '"' + os.path.join(os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logs'), 'logs.txt') + '"'
LOG_FILE_PATH2 = '"' + os.path.join(os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logs2'), 'logs2.txt') + '"'
LOG_FILE_NAME = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'logging.conf')
FLOOD_TIME = 1000
HAYSTACK_SITECONF = 'dinette.search'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'index.db')
SITE_URL = 'http://127.0.0.1:8000'