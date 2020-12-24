# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/fetch.py
# Compiled at: 2016-02-28 23:09:36
"""
Fetches a folder of book files from a remote to local
"""
from __future__ import print_function
import os, sh

class BookFetcher:
    """ A BookFetcher:
        - makes a shelf (folder in library directory)
        - rsyncs the book from PG to the shelf
    """

    def __init__(self, book):
        self.book = book

    def fetch(self):
        self.make_local_path()
        self.fetch_remote_book_to_local_path()

    def make_local_path(self):
        try:
            try:
                os.makedirs(self.book.local_path)
            except OSError:
                print(('Folder {0} already exists').format(self.book.local_path))

        finally:
            os.chmod(self.book.local_path, 511)

    def fetch_remote_book_to_local_path(self):
        sh.rsync('-rvhz', ('ftp@gutenberg.pglaf.org::gutenberg/{0}').format(self.book.remote_path), self.book.local_path + '/', '--exclude-from=exclude.txt')