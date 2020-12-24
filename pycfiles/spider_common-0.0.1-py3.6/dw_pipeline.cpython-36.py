# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/spider_common/persistent/scrapy/pipelines/dw_pipeline.py
# Compiled at: 2019-04-16 05:50:15
# Size of source mod 2**32: 1608 bytes
from ..dw_logger import DwLogger
from parser_engine.itemclassloader import ItemClassLoader
from parser_engine.utils import load_scrapy_settings
from spider_common.common_utils.exceptions import InitArgsException

class DwPipeline(object):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = cls(settings=(crawler.settings))
        return obj

    def __init__(self, action=None, item_cls=None, settings=None):
        self.item_loader = None
        self.logger = None
        self.item_configs = None
        self.setup_from_settings(settings=(settings if settings else load_scrapy_settings()))
        if action:
            if item_cls:
                cls = self.item_loader.load(item_cls)
                self.item_configs.update({action: cls})

    def setup_from_settings(self, settings):
        self.item_loader = ItemClassLoader(settings=settings)
        self.logger = DwLogger(settings=settings)
        conf = settings.get('DW_ITEMS_CONFIG')
        if conf:
            item_configs = {}
            for action, item_cls in conf.items():
                cls = self.item_loader.load(item_cls)
                if not cls:
                    raise InitArgsException('item class %s not found' % item_cls)
                item_configs[action] = cls

            self.item_configs = item_configs

    def process_item(self, item, spider):
        if self.item_configs:
            for action, item_cls in self.item_configs.items():
                if isinstance(item, item_cls):
                    (self.logger.log_to_dw)(action, **item)

        return item