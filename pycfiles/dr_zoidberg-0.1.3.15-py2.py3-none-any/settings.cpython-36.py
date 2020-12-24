# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ginopalazzo/Magic/zoidberg/zoidberg/scraper/settings.py
# Compiled at: 2018-03-14 10:32:53
# Size of source mod 2**32: 3287 bytes
BOT_NAME = 'scraper'
SPIDER_MODULES = [
 'scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
COUNTRIES = [
 'es']
USER_AGENT = 'zoidberg (+https://www.github.com/ginopalazzo/zoidberg)'
ROBOTSTXT_OBEY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_DEBUG = False