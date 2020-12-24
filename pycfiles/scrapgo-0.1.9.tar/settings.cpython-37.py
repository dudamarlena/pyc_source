# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\settings.py
# Compiled at: 2019-05-26 03:36:33
# Size of source mod 2**32: 714 bytes
import os
from datetime import timedelta
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER_AGENT_NAME = 'chrome'
REQUEST_DELAY = 0.5
RETRY_INTERVAL_SECONDS = (10, 100, 1000)
CACHE_NAME = 'REQUEST_CACHE'
CACHE_BACKEND = 'sqlite'
CACHE_EXPIRATION = timedelta(days=100)
CACHE_METHODS = ('GET', 'POST')
BEAUTIFULSOUP_PARSER = 'html.parser'
CRAWL_TARGET_ATTRS = ('href', 'src')
PARSE_CONTENT_TYPES = [
 'text/css', 'text/html', 'text/javascript', 'text/plain', 'text/xml']
URLPATTERN_DISPATCHER = 'urlpattern'
REDUCER_DISPATCHER = 'reducer'
URLFILTER_DISPATCHER = 'urlfilter'
REDUCER_NAMESPACE = 'namespace'