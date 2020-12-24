# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./src/utils/update_checker.py
# Compiled at: 2020-03-23 16:21:35
# Size of source mod 2**32: 853 bytes
import logging, requests
from ..assets.version import get_value
from ..core.display import new_version_news
logger = logging.Logger('UPDATE_CHECK')
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'

def check_updates():
    try:
        logger.info('Checking latest version')
        pypi_short_url = 'http://bit.ly/2yYyFGd'
        headers = {'User-Agent': user_agent}
        res = requests.get(pypi_short_url, verify=False, headers=headers,
          timeout=3)
        latest_version = res.json()['info']['version']
        if get_value() != latest_version:
            new_version_news(latest_version)
    except Exception:
        logger.warn('Failed to check for update')