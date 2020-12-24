# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/easyspider/core/easyEngine.py
# Compiled at: 2017-08-03 10:12:10
from scrapy.core.engine import ExecutionEngine
from scrapy.utils.misc import load_object
import logging
logger = logging.getLogger(__name__)
scraper_key = 'SCRAPER'
default_scraper = 'scrapy.core.scraper.Scraper'

class easyEngine(ExecutionEngine):

    def __init__(self, crawler, spider_closed_callback):
        super(easyEngine, self).__init__(crawler, spider_closed_callback)
        scraper = self.settings.get(scraper_key, default_scraper)
        scraper_cls = load_object(scraper)
        self.scraper = scraper_cls(crawler)