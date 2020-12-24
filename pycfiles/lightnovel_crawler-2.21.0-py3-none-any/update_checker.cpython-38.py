# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\src\utils\update_checker.py
# Compiled at: 2020-03-25 09:13:24
# Size of source mod 2**32: 694 bytes
import logging, cloudscraper
from assets.version import get_value
from core.display import new_version_news
logger = logging.Logger('UPDATE_CHECK')

def check_updates():
    try:
        logger.info('Checking latest version')
        pypi_short_url = 'http://bit.ly/2yYyFGd'
        scraper = cloudscraper.create_scraper()
        res = scraper.get(pypi_short_url, timeout=5)
        latest_version = res.json()['info']['version']
        if get_value() != latest_version:
            new_version_news(latest_version)
    except Exception:
        logger.warn('Failed to check for update')