# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jess/.local/conda/lib/python3.6/site-packages/earthchem/pagination.py
# Compiled at: 2018-06-02 08:11:53
# Size of source mod 2**32: 977 bytes
""" file:   requests.py
    author: Jess Robertson, CSIRO Minerals
    date:   May 2018

    description: Pagination utilities
"""
from itertools import takewhile, count

def make_pages(max_items, items_per_page=50):
    """ Get a list of page bounds for submitting to the REST endpoint
        
        Parameters:
            max_items - the total number of items to get
            items_per_page - the size of each page (defaults to 50 which is 
                the Earthchem default)
        
        Returns:
            a list of tuples with (start_row, end_row) for each page
    """
    page_bounds = lambda n: (
     n * items_per_page, (n + 1) * items_per_page - 1)
    pages = list(takewhile(lambda x: x[0] < max_items, map(page_bounds, count())))
    pages[-1] = (
     pages[(-1)][0], max_items)
    return pages