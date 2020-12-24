# uncompyle6 version 3.7.4
# PyPy Python bytecode 2.7 (62218)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wargaming/settings.py
# Compiled at: 2018-05-14 16:33:13
from wargaming.version import get_version
ALLOWED_GAMES = ('wot', 'wgn', 'wows', 'wotb', 'wotx', 'wowp')
ALLOWED_REGIONS = ('ru', 'asia', 'na', 'eu', 'xbox', 'ps4')
REGION_TLD_MAP = {'ru': 'ru', 
   'asia': 'asia', 
   'na': 'com', 
   'eu': 'eu'}
GAME_API_ENDPOINTS = {'wgn': 'https://api.worldoftanks.{region}/wgn/', 
   'wot': 'https://api.worldoftanks.{region}/wot/', 
   'wotb': 'https://api.wotblitz.{region}/wotb/', 
   'wotx': 'https://api-{region}-console.worldoftanks.com/wotx/', 
   'wowp': 'https://api.worldofwarplanes.{region}/wowp/', 
   'wows': 'https://api.worldofwarships.{region}/wows/'}
DEFAULT_REGION = 'ru'
ALLOWED_LANGUAGES = ('en', 'ru', 'pl', 'de', 'fr', 'es', 'zh-cn', 'tr', 'cs', 'th',
                     'vi', 'ko')
DEFAULT_LANGUAGE = 'en'
HTTP_USER_AGENT_HEADER = ('python-wargaming/{0} (https://github.com/svartalf/python-wargaming)').format(get_version())
RETRY_COUNT = 10