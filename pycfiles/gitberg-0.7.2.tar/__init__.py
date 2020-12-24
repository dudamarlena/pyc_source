# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/__init__.py
# Compiled at: 2019-08-12 15:45:37
"""
"""
from .book import Book
from .clone import clone
from .config import ConfigFile, check_config, NotConfigured
from .library import main as library
from .workflow import upload_all_books, upload_list, upload_book
__title__ = 'gitberg'
__appname__ = 'gitberg'
__version__ = '0.6.3'
__copyright__ = 'Copyright 2012-2018 Seth Woodworth and the Free Ebook Foundation'