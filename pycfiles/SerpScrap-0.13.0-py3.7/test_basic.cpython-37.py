# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_basic.py
# Compiled at: 2018-10-01 04:06:18
# Size of source mod 2**32: 1689 bytes
import datetime, os, random
from serpscrap.config import Config
from serpscrap.serpscrap import SerpScrap

class TestClass:
    keyword_list = [
     'computer news',
     'since topics',
     'python tutorial',
     'pythons',
     'machine learning',
     'artificial intelligence']

    def test_config_default(self):
        config = Config()
        assert len(config.get()) == 32
        assert config.use_own_ip is True
        assert config.screenshot is True
        assert config.scrape_urls is False
        today = datetime.datetime.strftime(datetime.datetime.utcnow(), '%Y-%m-%d')
        assert config.today == today

    def test_simple(self):
        keywords = random.choice(self.keyword_list)
        config = Config()
        scrap = SerpScrap()
        scrap.init(config=(config.get()), keywords=keywords)
        results = scrap.run()
        assert len(results) > 0
        assert len(results[0]) > 0

    def test_screenshot(self):
        keywords = random.choice(self.keyword_list)
        config = Config()
        config.set('screenshot', True)
        scrap = SerpScrap()
        scrap.init(config=(config.get()), keywords=keywords)
        screendir = '{}/{}'.format(config.get()['dir_screenshot'], config.today)
        assert config.get()['screenshot'] is True
        assert os.path.exists(screendir) is True