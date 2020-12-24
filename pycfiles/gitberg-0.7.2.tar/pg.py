# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/util/pg.py
# Compiled at: 2018-10-01 17:31:41
import os

def source_start(base='', book_id='book'):
    """
    chooses a starting source file in the 'base' directory for id = book_id
    
    """
    repo_htm_path = ('{book_id}-h/{book_id}-h.htm').format(book_id=book_id)
    possible_paths = ['book.asciidoc',
     repo_htm_path,
     ('{}-0.txt').format(book_id),
     ('{}-8.txt').format(book_id),
     ('{}.txt').format(book_id),
     ('{}-pdf.pdf').format(book_id)]
    for path in possible_paths:
        fullpath = os.path.join(base, path)
        if os.path.exists(fullpath):
            return path

    return