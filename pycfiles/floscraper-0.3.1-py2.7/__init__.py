# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\floscraper\__init__.py
# Compiled at: 2019-08-03 21:36:40
"""
A scraper utility package
"""
__author__ = 'the01'
__email__ = 'jungflor@gmail.com'
__copyright__ = 'Copyright (C) 2014-19, Florian JUNG'
__license__ = 'MIT'
__version__ = '0.3.1'
__date__ = '2019-08-04'
from .webscraper import WebScraper, default_user_agents, WEBConnectException, WEBFileException, WEBParameterException
from .cache import Cache
from .models import Response, CacheInfo
__all__ = [
 'webscraper', 'WebScraper', 'Cache', 'Response', 'CacheInfo']