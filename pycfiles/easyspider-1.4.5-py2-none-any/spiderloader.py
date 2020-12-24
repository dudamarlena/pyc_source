# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zhanghang/Desktop/workspace/molbase/molbase_2017_7_3/release/easyspider/core/spiderloader.py
# Compiled at: 2018-03-11 12:15:05
from __future__ import absolute_import
import warnings, traceback
from scrapy.utils.misc import walk_modules
from scrapy.spiderloader import SpiderLoader

class easySpiderLoader(SpiderLoader):

    def _load_all_spiders(self):
        for name in self.spider_modules:
            try:
                for module in walk_modules(name):
                    reload(module)
                    self._load_spiders(module)

            except ImportError:
                if self.warn_only:
                    msg = ("\n{tb}Could not load spiders from module '{modname}'. See above traceback for details.").format(modname=name, tb=traceback.format_exc())
                    warnings.warn(msg, RuntimeWarning)
                else:
                    raise

        try:
            self._check_name_duplicates()
        except AttributeError:
            pass