# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/c24b/projets/crawtext/newspaper/settings.py
# Compiled at: 2014-11-06 08:50:33
__doc__ = '\nUnlike configuration.py, this file is meant for static, entire project\nencompassing settings, like memoization and caching file directories.\n'
__title__ = 'newspaper'
__author__ = 'Lucas Ou-Yang'
__license__ = 'MIT'
__copyright__ = 'Copyright 2014, Lucas Ou-Yang'
import logging, os
from cookielib import CookieJar as cj
from .version import __version__
log = logging.getLogger(__name__)
PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
POPULAR_URLS = os.path.join(PARENT_DIRECTORY, 'resources/misc/popular_sources.txt')
USERAGENTS = os.path.join(PARENT_DIRECTORY, 'resources/misc/useragents.txt')
STOPWORDS_DIR = os.path.join(PARENT_DIRECTORY, 'resources/text')
NLP_STOPWORDS_EN = os.path.join(PARENT_DIRECTORY, 'resources/misc/stopwords-nlp-en.txt')
DATA_DIRECTORY = '.newspaper_scraper'
TOP_DIRECTORY = os.path.join(os.path.expanduser('~'), DATA_DIRECTORY)
if not os.path.exists(TOP_DIRECTORY):
    os.mkdir(TOP_DIRECTORY)
LOGFILE = os.path.join(TOP_DIRECTORY, 'newspaper_errors_%s.log' % __version__)
MONITOR_LOGFILE = os.path.join(TOP_DIRECTORY, 'newspaper_monitors_%s.log' % __version__)
MEMO_FILE = 'memoized'
MEMO_DIR = os.path.join(TOP_DIRECTORY, MEMO_FILE)
if not os.path.exists(MEMO_DIR):
    os.mkdir(MEMO_DIR)
CF_CACHE_DIRECTORY = 'feed_category_cache'
ANCHOR_DIRECTORY = os.path.join(TOP_DIRECTORY, CF_CACHE_DIRECTORY)
if not os.path.exists(ANCHOR_DIRECTORY):
    os.mkdir(ANCHOR_DIRECTORY)
TRENDING_URL = 'http://www.google.com/trends/hottrends/atom/feed?pn=p1'