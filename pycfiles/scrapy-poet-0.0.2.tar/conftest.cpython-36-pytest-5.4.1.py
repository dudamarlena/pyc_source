# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kmike/svn/scrapy-poet/tests/conftest.py
# Compiled at: 2020-04-27 13:38:41
# Size of source mod 2**32: 445 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from scrapy.settings import Settings

@pytest.fixture()
def settings(request):
    """ Default scrapy-poet settings """
    s = dict(ITEM_PIPELINES={'tests.utils.CollectorPipeline': 100},
      DOWNLOADER_MIDDLEWARES={'scrapy_poet.InjectionMiddleware': 543})
    return Settings(s)