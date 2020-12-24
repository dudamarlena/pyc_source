# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/Obsidian/spiders/jsonspider.py
# Compiled at: 2018-01-07 08:54:46
# Size of source mod 2**32: 756 bytes
from Obsidian.ddspider import DDSpider
from Obsidian.ddsourcejsonconfig import DDSourceJsonConfig

class JsonSpider(DDSpider):
    name = 'jsonspider'

    def __init__(self, path='config.json', **kwargs):
        (super().__init__)(**kwargs)
        config = DDSourceJsonConfig(path)
        self.allowed_domains = config.allowed_domains
        self.start_urls = config.start_urls
        self.prefix = config.prefix
        self.link_array_pipline = config.link_array_pipline
        self.main_content_pipline = config.main_content_pipline
        self.item_pipline = config.item_pipline