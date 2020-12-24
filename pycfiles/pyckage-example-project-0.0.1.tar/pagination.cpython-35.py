# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /MyWork/Projects/PyCK/pyck/lib/pagination.py
# Compiled at: 2014-12-16 18:25:44
# Size of source mod 2**32: 1529 bytes


def get_pages(total_recs, current_page, recs_per_page=10, max_pages=10):
    """
    A utility function that returns the pages (for records pagination display purposes)

    :param total_recs:
        Total number of records
    :param current_page:
        Current page that is being displayed
    :param recs_per_page:
        Number of records being displayed per page
    :param max_pages:
        Maximum number of pages to return

    Returns a list containing pages that should be displayed as page links.
    """
    total_pages = int(total_recs / recs_per_page)
    if total_recs % recs_per_page > 0:
        total_pages += 1
    pages = []
    if 0 == max_pages % 2:
        pages_before = max_pages / 2 - 1
    else:
        pages_before = max_pages / 2
    pages_after = int(max_pages / 2)
    pages_before = int(pages_before)
    start_page = 1
    if total_pages <= max_pages:
        for i in range(1, total_pages + 1):
            pages.append(i)

    else:
        pages_left = max_pages - 1
        if current_page - pages_before <= 0:
            pages_before = current_page - 1
        if current_page + pages_after > total_pages:
            pages_before += current_page + pages_after - total_pages
        start_page = current_page - pages_before
        for i in range(start_page, current_page + 1):
            pages.append(i)
            pages_left -= 1
            start_page += 1

        for i in range(pages_left + 1):
            pages.append(start_page)
            start_page += 1

    return pages