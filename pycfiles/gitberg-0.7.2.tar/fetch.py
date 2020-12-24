# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/fetch.py
# Compiled at: 2018-10-03 15:32:10
"""
Fetches a folder of book files from a remote to local
"""
import os, sh
from .parameters import PG_RSYNC

class BookFetcher:
    """ A BookFetcher:
        - makes a shelf (folder in library directory)
        - rsyncs the book from PG to the shelf
    """

    def __init__(self, book):
        self.book = book

    def fetch(self):
        self.fetch_remote_book_to_local_path()

    def fetch_remote_book_to_local_path(self):
        sh.rsync('-rvhz', ('{}{}').format(PG_RSYNC, self.book.remote_path), self.book.local_path + '/', '--exclude-from=exclude.txt')